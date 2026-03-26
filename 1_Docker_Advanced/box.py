import os
import ctypes
import json
import argparse


CLONE_NEWUTS = 0x04000000
CLONE_NEWNS  = 0x00020000
CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL("libc.so.6")


def preparation(id):
    location = f"/var/lib/box/{id}"
    u, w, m = f"{location}/upper", f"{location}/work", f"{location}/merged"
    for d in [u, w, m]:
        os.makedirs(d, exist_ok=True)
    return u, w, m


def create_namespace():
    flags = CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWPID
    if libc.unshare(flags) != 0:
        raise Exception("Failed to create namespace")
    # return flags


def mount_overlay(lower, upper, work, merged):
    options = f"lowerdir={lower},upperdir={upper},workdir={work}".encode()
    rez = libc.mount(b"overlay", merged.encode(), b"overlay", 0, options)
    if rez != 0:
        raise Exception("Failed to mount overlay")
    # return rez


def run_box(id, config):
    u, w, m = preparation(id)
    lower = os.path.abspath(config['lowerdir'])
    create_namespace()
    pid = os.fork()
    if pid > 0:
        os.waitpid(pid, 0)
    else:
        try:
            mount_overlay(lower, u, w, m)
            os.chroot(m)
            os.chdir("/")
            libc.mount(b"proc", b"/proc", b"proc", 0, None)
            hostname = config['hostname'].encode()
            libc.sethostname(hostname, len(hostname))
            cmd = config['command']
            os.execvp(cmd, [cmd])
        except Exception as e:
            print(f"Error inside container: {e}")
            os._exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--id", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    if args.command == "run":
        with open(args.config, 'r') as f:
            conf = json.load(f)
        run_box(args.id, conf)

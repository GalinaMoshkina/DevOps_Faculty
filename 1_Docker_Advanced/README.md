# Лабораторная работа №1 - Docker
## Advanced-трэк. Вариант 2
### Выполняла Мошкина Галина Андреевна, 466780
<img width="736" height="552" alt="image" src="https://github.com/user-attachments/assets/34f365bb-ea9b-4043-a1d3-518559b00330" />

**Результат**: утилита на Python, которая запускает команду в контейнере.  

Для начала **подготовила среду для работы**: узнала, какую версию mini root filesystem мне необходимо скачать с помощью команды ```uname -m``` - отображает сведения о системе. Устанавливаем x86_64. Распаковываем архив с помощью ```tar```  
<img width="581" height="102" alt="image" src="https://github.com/user-attachments/assets/c4a38dfa-780c-42a0-b5a6-63fd637aba10" />   
  
  
```(base) gala@gala-NMH-WDX9:~/Documents/DevopsElective/lab1$ sudo tar -xzvf alpine-minirootfs-3.23.3-x86_64.tar.gz -C ./alpine_base```    
<img width="924" height="526" alt="image" src="https://github.com/user-attachments/assets/372ccf24-ffd9-4d5e-b246-41f35dc8232a" />   
Все отлично, база готова.   
Создаем ```config.json``` - конфигурационный файл   
В качестве нижнего слоя у меня базовая файловая система Alpine.   
```
{
  "command": "/bin/sh",
  "hostname": "box-container",
  "lowerdir": "/home/gala/Documents/DevopsElective/lab1/alpine_base"
}
```
```command``` - команда для запуска внутри контейнера  
```hostname``` - имя контейнера в UTS namespace  
```lowerdir``` - путь к базовой файловой системе - Alpine Linux  

**Написание скрипта**  
Перейдем к написанию ```box.py```. Задачи скрипта:   
1. OverlayFS - для создания слоистой файловой системы  
2. Namespaces - для изоляции процессов, файловой системы и hostname  
3. Chroot - для изменения корневой директории  
   
Для начала напишем программу для создания необходимых папок для контейнеров - сформируем **OverlayFS**.  
В /var/lib/box будут храниться все контейнеры, а вних уже будут создаваться нужные папки для OverlayFS: upper, work, merged.  
```
import os


def preparation(id):
    location = f"/var/lib/box/{id}"
    os.makedirs(f"{location}/upper", exist_ok=True)
    os.makedirs(f"{location}/work", exist_ok=True)
    os.makedirs(f"{location}/merged", exist_ok=True)
    return f"{location}/upper", f"{location}/work", f"{location}/merged"

preparation("test1")
```
  
<img width="633" height="142" alt="image" src="https://github.com/user-attachments/assets/db9489ff-7c41-4ef7-acfb-fc233e9f4351" />  
  
Работает!  
Далее переходим к созданию **namespaces**  
```
import os
import ctypes


CLONE_NEWUTS = 0x04000000
CLONE_NEWNS  = 0x00020000
CLONE_NEWPID = 0x20000000
libc = ctypes.CDLL("libc.so.6")


def preparation(id):
    location = f"/var/lib/box/{id}"
    os.makedirs(f"{location}/upper", exist_ok=True)
    os.makedirs(f"{location}/work", exist_ok=True)
    os.makedirs(f"{location}/merged", exist_ok=True)
    return f"{location}/upper", f"{location}/work", f"{location}/merged"


def create_namespace():
    flags = CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWPID
    if libc.unshare(flags) != 0:
        raise Exception("Failed to create namespace")
    return flags
```
```CLONE_NEW[...]``` - флажки/числовые идентификаторы. ```ctypes.CDLL("libc.so.6")``` загружает системный файл, в котором реализованы функции unshare, mount, fork и другие.  
  
Реализуем функцию **mount_overlay**  
```
def mount_overlay(lower, upper, work, merged):
    options = f"lowerdir={lower},upperdir={upper},workdir={work}".encode()
    rez = libc.mount(b"overlay", merged.encode(), b"overlay", 0, options)
    if rez != 0:
        raise Exception("Failed to mount overlay")
    return rez
```
Проверим, работает ли  
<img width="1847" height="1037" alt="image" src="https://github.com/user-attachments/assets/8b04d848-2649-497c-866a-62da9f310179" />  
Всё круто, вывод последней команды ps aux означает, что изоляция процессов не завершена. Чтобы контейнер стал полностью изолированным, как и в Docker, нам нужно примонтировать новую файловую систему /proc специально для этого контейнера.  

Теперь **финальный код**  
```
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

```
Ииии...  
<img width="1444" height="288" alt="image" src="https://github.com/user-attachments/assets/d01ed860-b87e-4350-bff4-9d511fdeb44c" />  
**РАБОТАЕТ!**  
<img width="640" height="352" alt="image" src="https://github.com/user-attachments/assets/880f5d4b-43c1-4c11-afef-0ef14b84a96a" />  

```ps aux``` - проверили изоляцию процессов, а именно видны только процессы контейнера. ```hostname``` - проверка работы namespaces, тоже корректно. На ```ls /``` вывод - структура директорий Alpine Linux, все верно. Монтирование proc filesystem работает.  
  
**Про проверку кода**  
Сначала я парсила аргументы командной строки, затем читается config.json (args.config - путь к файлу config.json). Затем уже вызов run_box.  
  
**Про run_box**  
Сначала нужно было подготовить директории - пункт OverlayFS. Затем - Namespaces.    
Далее я создала дочерний процесс с помощью команды ```os.fork()``` - создает точную копию текущего процесса (дочерний процесс), работающую параллельно с родительским. После ```os.fork()``` дочерний процесс становится PID 1 в новом PID namespace. Родительский процеес блокируется, пока контейнер не завершится.  
Далее контейнеризация!  
Идет монтирование OverlayFS - появляется полная файловая система с возможностью записи.  
```chroot(m)``` - делает merged новой корневой директорией ```/```. ```chdir("/")``` - переходит в новый корень.  
Для ```ps aux```: ```/proc``` - виртуальная файловая система с информацией о процессах.  
Для hostname устанавливается имя контейнера в UTS namespace - берется из ```config.json```.  
<img width="851" height="644" alt="image" src="https://github.com/user-attachments/assets/a623995a-883a-4afb-81f2-7666dfcd16ed" />  

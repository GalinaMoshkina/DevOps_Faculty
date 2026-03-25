# Лабораторная работа №1 - Docker
## Advanced-трэк. Вариант 2
### Выполняла Мошкина Галина Андреевна, 466780
Результат: утилита на Python, которая запускает команду в контейнере.  

Для начала подготовила среду для работы: узнала, какую версию mini root filesystem мне необходимо скачать с помощью команды ```uname -m``` - отображает сведения о системе. Устанавливаем x86_64. Распаковываем архив с помощью ```tar```  
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
  "lowerdir": "alpine_base"
}
```
Перейдем к написанию ```box.py```. Задачи скрипта:   
1. Парсинг данных   
2. OverlayFS   
3. Namespaces   
4. Запуск утилиты   
   
Для начала напишем программу для создания необходимых папок для контейнеров - сформируем OverlayFS.  
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
Далее переходим к созданию namespaces  
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
CLONE_NEW[...] - флажки/числовые идентификаторы. ctypes.CDLL("libc.so.6") загружает системный файл, в котором реализованы функции unshare, mount, fork и другие.  
  
Реализуем функцию mount  
```
def mount(lower, upper, work, merged):
    options = f"lowerdir={lower},upperdir={upper},workdir={work}".encode()
    rez = libc.mount(b"overlay", merged.encode(), b"overlay", 0, options)
    if rez != 0:
        raise Exception("Failed to mount overlay")
    return rez
```
Объясню  
Проверим, работает ли  
<img width="1847" height="1037" alt="image" src="https://github.com/user-attachments/assets/8b04d848-2649-497c-866a-62da9f310179" />  
Всё круто, вывод последней команды ps aux означает, что изоляция процессов не завершена. Чтобы контейнер стал полностью изолированным, как и в Docker, нам нужно примонтировать новую файловую систему /proc специально для этого контейнера.  


объясняю еще  
<img width="1444" height="288" alt="image" src="https://github.com/user-attachments/assets/d01ed860-b87e-4350-bff4-9d511fdeb44c" />  
ГООООООООЛ  



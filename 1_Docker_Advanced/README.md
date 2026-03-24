# Лабораторная работа №1 - Docker
## Advanced-трэк. Вариант 2
### Выполняла Мошкина Галина Андреевна, 466780
Результат: утилита на Python, которая запускает команду в контейнере.  

Для начала подготовила среду для работы: узнала, какую версию mini root filesystem мне необходимо скачать с помощью команды ```uname -m``` - отображает сведения о системе. Устанавливаем x86_64. Распаковываем архив с помощью ```tar```  
<img width="581" height="102" alt="image" src="https://github.com/user-attachments/assets/c4a38dfa-780c-42a0-b5a6-63fd637aba10" />   
  
  
```(base) gala@gala-NMH-WDX9:~/Documents/DevopsElective/lab1$ sudo tar -xzvf alpine-minirootfs-3.23.3-x86_64.tar.gz -C ./alpine_base```    
<img width="924" height="526" alt="image" src="https://github.com/user-attachments/assets/372ccf24-ffd9-4d5e-b246-41f35dc8232a" />   
Все отлично, база готова.   

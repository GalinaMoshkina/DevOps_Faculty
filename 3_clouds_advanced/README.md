<img width="736" height="740" alt="image" src="https://github.com/user-attachments/assets/72817c60-501e-4649-8708-7f2a35124b70" /># Лабораторная работа №3 - Облако
## Advanced-трэк. Вариант 2 - Использование DevOps-инструментов
### Выполняла Мошкина Галина Андреевна, 466780
Нужно установить MinIO с помощью Ansible плейбука на виртуальную машину, созданную с помощью Terraform.  
Terraform будет обеспечивать ресурсы для работы, Ansible плейбук уже нужен для конфигурации ресурсов и как раз для установки MinIO.  
Тогда первым делом устанавливаем Terraform:  
<img width="1164" height="192" alt="image" src="https://github.com/user-attachments/assets/58d3c2fb-99f2-41a8-96eb-2db7b071d895" />  
Проверим, работает ли, создав файл `main.tf`:  
<img width="1164" height="192" alt="image" src="https://github.com/user-attachments/assets/f0487bf2-24ff-4e14-9680-f27071a347b5" />  
Далее прописываем `terraform init` - инициализация работы, и `terraform apply` - применение изменений 
<img width="963" height="357" alt="image" src="https://github.com/user-attachments/assets/8cd64613-4697-4325-bd48-abee7c57ba5f" />  
<img width="1474" height="521" alt="image" src="https://github.com/user-attachments/assets/9a97488b-5f66-4ff0-a7e2-f19211c3a469" />  
Удаляем файл с помощью команды `rm main.tf` и приступаем уже к заданию лабораторной  
<img width="720" height="591" alt="image" src="https://github.com/user-attachments/assets/705a5091-86bc-4287-adf0-518acf319a95" />  
Далее переходим к облачной части. Я решила, что не хочу никак взаимодействовать с yandex cloud. Поэтому было решено развернуть у себя openstack. Я решила воспользоваться DevStack, так как он требует меньше всего ресурсов, для учебной задачи это то, что нужно.  
Идем четко по туториалу [отсюда](https://docs.openstack.org/devstack/latest/): создаем пользователя `stack`, ему дали права суперпользователя, а затем переводимся сами на пользователя stack, перешли в папку `devstack`.  
<img width="1223" height="448" alt="image" src="https://github.com/user-attachments/assets/8ab0b733-6a81-4fbf-a2d5-f9eb2029ffd8" />  
Затем необходимо создать файл `local.conf` со следующим содержимым:  
```
[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
```
Прописываем команду `./stack.sh` для установки  
Далее для авторизации в облаке OpenStack и проверки статуса его компонентов запускаем данные команды:  
```
source openrc admin admin
openstack service list
```  
<img width="696" height="61" alt="image" src="https://github.com/user-attachments/assets/9f79ec45-65a4-413f-8a87-f39d3e9676d6" />  
<img width="736" height="740" alt="image" src="https://github.com/user-attachments/assets/69f51b9e-8f2b-4404-8b7d-39d5044b4348" />  
Проверяем логи  
```
stack@gala-NMH-WDX9:~/devstack$ /opt/stack/logs/worlddump-2026-05-16-195704.txt
-bash: /opt/stack/logs/worlddump-2026-05-16-195704.txt: Permission denied
```
<img width="1114" height="411" alt="image" src="https://github.com/user-attachments/assets/8d04d27d-a4bb-473a-a652-fc5ed2220c87" />  
Ресурсов на работу DevStack почти нет, он упал до запуска сервисов.  
Я решила, что обойдусь без DevStack в данной работе, так как ТЗ не требует реального облака.  






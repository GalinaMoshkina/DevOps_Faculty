
1 Установка  
  
<img width="1484" height="409" alt="image" src="https://github.com/user-attachments/assets/5d6e5277-36ac-4bb6-a97b-2ad3a7d641aa" />  
<img width="1197" height="74" alt="image" src="https://github.com/user-attachments/assets/1a7fafb6-7461-44be-bf9b-399597680458" />  

kuberctl  
<img width="1164" height="388" alt="image" src="https://github.com/user-attachments/assets/f13fec74-dac7-4876-9526-6463667a89c1" />

<img width="1472" height="806" alt="image" src="https://github.com/user-attachments/assets/5c85c9d4-233d-45fa-962b-27b29c4599c6" />  

<img width="655" height="95" alt="image" src="https://github.com/user-attachments/assets/20101754-853c-41ce-a073-cfa6f6a0524a" />  
Открыли дашборд с помощью команды ```minikube dashboard```, выбрали all namespaces  
Видно etcd БД, controller manager, scheduler, api server  
<img width="1843" height="987" alt="image" src="https://github.com/user-attachments/assets/c1dbfd34-a6a7-4654-9498-c90a67b4dc66" />  

Перейдем к написанию ```deployment.yaml```. Во первых, в kubernetis всё общение происходит через API, сл-но, указываем ```apiVersion```



Запуск!

<img width="1322" height="444" alt="image" src="https://github.com/user-attachments/assets/fefa7f55-b07c-46ac-9df5-0dc84e73151e" />  
Команды  
```kubectl apply -f /home/gala/.vscode/2course/DevOps/2_kuber_base/deployment.yaml```  
```kubectl apply -f /home/gala/.vscode/2course/DevOps/2_kuber_base/service.yaml```  
```kubectl get pods```
```kubectl get services```

<img width="1847" height="583" alt="image" src="https://github.com/user-attachments/assets/ae023c60-8892-40be-805c-a8efacc9c85c" />  

Гол  
<img width="1322" height="444" alt="image" src="https://github.com/user-attachments/assets/45037ef6-73e6-4578-ba79-c62abf52d0e7" />  
<img width="1230" height="350" alt="image" src="https://github.com/user-attachments/assets/b292a1df-a205-4216-adc5-eec1428b819d" />  
ура  
<img width="1847" height="980" alt="image" src="https://github.com/user-attachments/assets/95ceec90-66b2-4635-a623-9ce8f9afb64e" />  

<img width="1323" height="426" alt="image" src="https://github.com/user-attachments/assets/010cd491-89f4-4242-a967-a4b8e9c220f3" />  
<img width="1323" height="426" alt="image" src="https://github.com/user-attachments/assets/ca3e9441-b3f0-4b25-bbc4-4cbd5258af8f" />  
<img width="1331" height="533" alt="image" src="https://github.com/user-attachments/assets/4ea17f50-87ab-46d2-92a2-e3e3b3323218" />  




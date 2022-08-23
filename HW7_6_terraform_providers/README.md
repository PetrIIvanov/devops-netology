<h1>"7.6. Написание собственных провайдеров для Terraform." - Петр Иванов</h1>

Бывает, что 
* общедоступная документация по терраформ ресурсам не всегда достоверна,
* в документации не хватает каких-нибудь правил валидации или неточно описаны параметры,
* понадобиться использовать провайдер без официальной документации,
* может возникнуть необходимость написать свой провайдер для системы используемой в ваших проектах.   

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[https://github.com/hashicorp/terraform-provider-aws.git](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  


1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе. 


[data_source](https://github.com/hashicorp/terraform-provider-aws/blob/ba986c9ec5fc1db0e8deb4028e799e05be1bfa35/internal/provider/provider.go#L414)
[resourse](https://github.com/hashicorp/terraform-provider-aws/blob/ba986c9ec5fc1db0e8deb4028e799e05be1bfa35/internal/provider/provider.go#L922)

 
1. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
    * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.

name и name_prefix [конфликтуют](https://github.com/hashicorp/terraform-provider-aws/blob/632cff7679cb6e1e14076b9aac3e68b73f584b70/internal/service/sqs/queue.go#L82)
друг с другом



    * Какая максимальная длина имени? 

80 символов для обычной очереди и 75 для fifo (ну или обе по 80, но свободная часть меньше)


    * Какому регулярному выражению должно подчиняться имя? 
	

[ссылка](https://github.com/hashicorp/terraform-provider-aws/blob/632cff7679cb6e1e14076b9aac3e68b73f584b70/internal/service/sqs/queue.go#L424)

латинские буквы большие и маленькие, цифры и -
fifo очередь оканчиватеся на .fifo


	
	


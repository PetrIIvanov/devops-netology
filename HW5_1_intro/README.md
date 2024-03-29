<h1>"5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения." - Петр Иванов</h1>

## Задача 1

Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.

## Задача 1 - решение
~~~
Полная - это специализированная OS под задачи виртуализации
Паравиртуализация - это запуск виртуальных машин поверх обычной OS общего назначения 
Виртуализация на основе ОС - это изолирование процессов одной ОС друг от друга таким образом, чтобы они не догадывались о существовании друг друга.
~~~

Доработка
~~~
Обычная виртуализация: железо <-> ядро гипервизора <-> ядро VM
Паравиртуализация: железо <-> ядро хоста <-> ядро гипервизора <-> ядро VM

Вставляется ещё один преобразующий слой системных вызовов. Это раз. 
Два - хостовая ОС управляет памятью и дисковой/файловой системой, поэтому гипервизор во многом полагается
на механизмы, которые сделаны под другие задачи.   
~~~

## Задача 2

Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:
- физические сервера,
- паравиртуализация,
- виртуализация уровня ОС.

Условия использования:
- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения.
- Windows системы для использования бухгалтерским отделом.
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

## Задача 2 - решение

Высоконагруженная база данных, чувствительная к отказу.  
~~~
Полная виртуализация. + Какой-нибудь High Availability режим. + репликация 
Если база очень нагружена, то можно в сетапе одна VM на одном сервере. 
~~~

Различные web-приложения.
~~~
В контейнеры
~~~

Windows системы для использования бухгалтерским отделом
~~~
Полная виртуализация. Базы одельно, приложения отдельно. Бекап. 
~~~

Системы, выполняющие высокопроизводительные расчеты на GPU
~~~
Физический сервер + докер c драйверами, TensorFlow/PyTourch. GPU при расчётах нельзя делить, там и так всё под 80-100% забито. Но версию окружения проще в докере иметь.  
~~~


## Задача 3

Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

1. 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий.
~~~
*** VMWare VSphere + несколько ESXi. почему не Hyper-V ? потому что я его не знаю. Да и потом сегодня windows-based, завтра SQL server на Linux. Больше пространства будет для манёвра.
~~~

2. Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин.
~~~
*** Из бесплатного вроде только Xen/KVM есть. Значит будем его мучать.  
~~~


3. Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.
~~~
*** См. пп. 3, но наверное уже без KVM. 
~~~


4. Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.
~~~
*** Набрать докер-контейнеров и запускать в них. 
~~~



## Задача 4

Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.

## Задача 4 - решение

~~~
Главный недостаток - невозможно переносить VM машины между системами и восстанавливаться из бекапа. Второй недостаток - нужно держать специалистов по нескольким средам. 
Или одного который знает всё. Это дорого. Поэтому лучше даже не начинать такое. 
Если же оказались в таком, например купили другую компанию, а там уже есть что-то. Так вот если оказались, 
я бы делал так. Если есть базы какие-то и их нельзя в лоб перенести, то развернул бы реплики зеркально на двух архитектурах программными средствами СУБД. 
Приложения бы перенёс на какую-то одну путём миграции докер-контейнеров. 
Мониторинг единый настроить не проблема.
~~~
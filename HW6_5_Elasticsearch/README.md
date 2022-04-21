<h1>"6.5. Elasticsearch" - Петр Иванов</h1>

## Задача 1

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

## Ответ на задачу 1

Dockerfile (параметры прокси замарчены)  

~~~Docker
# syntax = docker/dockerfile:1.3-labs

FROM centos:7 as builder
#ARG s_proxy
#ARG s_proxy_short
#ARG s_user
#ARG s_pw

RUN yum -y install sudo wget vim
RUN sudo yum makecache
RUN sudo yum -y install perl-Digest-SHA && \
#java install
sudo yum -y install java-1.8.0-openjdk  java-1.8.0-openjdk-devel

#path config
RUN <<EOF cat | sudo tee /etc/profile.d/java8.sh
export ES_JAVA_HOME=/usr/lib/jvm/jre-openjdk
export PATH=\$PATH:\$JAVA_HOME/bin
export CLASSPATH=.:\$JAVA_HOME/jre/lib:\$JAVA_HOME/lib:\$JAVA_HOME/lib/tools.jar
EOF

RUN source /etc/profile.d/java8.sh

RUN <<EOF cat | sudo tee /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/oss-7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF

##RUN export HTTPS_PROXY=s_proxy && \
##export HTTPS_PROXY=s_proxy

#RUN sudo yum clean all && sudo yum makecache

#proxy_settings
COPY ./yum.conf /etc/yum.conf

RUN sudo yum clean all && sudo yum makecache && \
        sudo yum -y install elasticsearch-oss

# return old settings
COPY ./yum_clear.conf /etc/yum.conf

FROM builder

RUN sudo systemctl enable --now elasticsearch

~~~


<ссылка на image>
https://hub.docker.com/layers/netologyelastic/blackskif/netologyelastic/



JSON

~~~json
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "AD-t2sWPQfu0nB8eVv46OQ",
  "version" : {
    "number" : "7.10.2",
    "build_flavor" : "oss",
    "build_type" : "rpm",
    "build_hash" : "747e1cc71def077253878a59143c1f785afa92b9",
    "build_date" : "2021-01-13T00:42:12.435326Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
~~~



## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных


Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?


## Решение задачи 2

~~~
[root@fb5e769b9086 ~]# curl -X GET "localhost:9200/_cat/indices/*?v=true&s=index&pretty"
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   ind-1 gfcw-WMFSR-jLZFl-BthSg   1   0          0            0       208b           208b
yellow open   ind-2 bxS3QbBzRqG213qyUNOztg   2   1          0            0       416b           416b
yellow open   ind-3 S1YORV_3TIGPg51_Fkod6g   4   2          0            0       832b           832b
~~~
  
~~~
[root@fb5e769b9086 ~]# curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 7,
  "active_shards" : 7,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 41.17647058823529
}
~~~
  
Индексы в жёлтом состоянии потому что у них должны быть реплики, а нода по факту одна на данный момент. А кластер желтый, потому что в нём есть жёлтые индексы.

~~~
[root@fb5e769b9086 ~]# curl -X DELETE "localhost:9200/ind-*?pretty"
~~~

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.


## Решение задачи 3
  
~~~
[root@fb5e769b9086 ~]# curl -X PUT "localhost:9200/_snapshot/my_repository?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/snapshots"
  }
}
'
{
  "acknowledged" : true
}
~~~



~~~
health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test  dNQlpd8-SficfJ7sTZavyg   1   0          0            0       208b           208b
~~~
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

FROM centos:7

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

RUN export HTTPS_PROXY="http://xxxxxxxxxxx" && \
export HTTPS_PROXY="http://xxxxxxxxxxxxxxx"


#proxy_settings
RUN sudo cp /etc/yum.conf /etc/yum.conf_bak && sudo echo proxy=http://xxxxxxxxxx >> /etc/yum.conf  && \
        sudo echo proxy_username=xxxxxxx >> /etc/yum.conf && \
        sudo echo proxy_password=xxxxxxxx >> /etc/yum.conf

RUN sudo yum clean all && sudo yum makecache

RUN sudo yum -y install elasticsearch-oss && sudo cp /etc/yum.conf_bak /etc/yum.conf

RUN sudo systemctl enable --now elasticsearch

~~~
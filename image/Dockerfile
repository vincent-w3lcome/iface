FROM centos:centos7
MAINTAINER YuWenMao Project

WORKDIR /

RUN yum -y update; yum clean all
RUN yum -y install epel-release iproute net-tools vim; yum clean all

ADD . /yuwenmao/iface
RUN yum -y install python34 python34-virtualenv python34-devel
RUN yum -y install gcc git mysql-community-server mysql-community-devel mariadb-devel
RUN virtualenv-3.4 /yuwenmao/iface/venv
RUN source /yuwenmao/iface/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /yuwenmao/iface/requirements.txt

ADD ./image/entrypoint.sh /yuwenmao/

ENTRYPOINT ["/yuwenmao/entrypoint.sh"]

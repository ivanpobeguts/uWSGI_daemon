FROM centos:7

RUN yum -y update && \
yum install epel-release -y && \
yum install python-pip python-devel nginx gcc -y && \
pip install uwsgi
# 项目dockerfile镜像文件
FROM centos:latest
RUN rm -rf /etc/yum.repos.d/* && curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo && yum clean all &&  yum install -y python38 sudo mysql-devel gcc python38-devel
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
ADD requirements.txt /opt/myblog/
RUN pip3.8 install -r /opt/myblog/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /opt/myblog/
# 开发环境
#EXPOSE 8000
#CMD ["python3.8","manage.py","runserver","0.0.0.0:8000"]
# 线上环境
RUN pip3.8 install uwsgi -r /opt/myblog/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8997
CMD ["uwsgi","--ini","/opt/myblog/other/uwsgi.ini"]
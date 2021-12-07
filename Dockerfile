FROM amazonlinux:latest

RUN yum update -y && \
yum install -y python3 python3-devel

WORKDIR /flaskblog

COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
EXPOSE 5000

CMD ["python3", "app.py", "runserver","--host", "0.0.0.0", "--port", "5000"]
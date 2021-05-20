FROM harbor.base-fx.com/itd/python:3.7.4

COPY pip.conf /etc/
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -U pip
RUN pip install -r requirements.txt

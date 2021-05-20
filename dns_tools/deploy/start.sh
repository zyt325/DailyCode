#!/bin/bash

#命令只执行最后一个,所以用 &&

python manage.py collectstatic --noinput &&
#python manage.py migrate &&
python manage.py runserver 0.0.0.0:8000

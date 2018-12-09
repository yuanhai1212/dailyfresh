# Author：logan
from  django.core.mail import send_mail
from celery import Celery
from django.conf import settings
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfreshh.settings")
django.setup()
#创建一个Celery类的实例对象
app = Celery("celery_tasks.tasks",broker='redis://127.0.0.1:6379/1')

#定时发送邮件
@app.task
def send_register_active_email(email,username,res):
    '''发送激活邮箱'''
    subject = '天天生鲜欢迎信息'
    message = ''
    htmlmessage = "<h1>%s,欢迎您成为天天生鲜注册会员</h1><br>请点一下链接激活</br><a herf='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>" % (username, res, res)
    sender = settings.EMAIL_FROM
    send_mail(subject, message, sender, recipient_list=[email], html_message=htmlmessage)

from celery import shared_task
import time

from django.core.mail import mail_managers
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from news_d3 import settings
from simpleapp.models import Category, Product
from news_d3.celery import app


@app.task
def send_email_task(pk):
    products = Product.objects.order_by('price')[:3]
    text = '\n'.join(['{} - {}'.format(p.name, p.price) for p in products])
    mail_managers("Самые дешевые товары", text)


@app.task
def weekly_send_task(pk):  # Запуск из celery
    products = Product.objects.order_by('price')[:3]
    text = '\n'.join(['{} - {}'.format(p.name, p.price) for p in products])
    mail_managers("Самые дешевые товары", text)

# class MyTasks(View):
#     def get(self, request):
#         # hello.delay()
#         # printer.delay(28)
#
#         printer.apply_async([10], countdown=5)
#         hello.delay()
#
#         return HttpResponse('Hello!')


# @shared_task
# def hello():
#     time.sleep(2)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)
#
#
# @shared_task
# def digit(n, c):
#     for i in range(n):
#         time.sleep(c)
#         print(i + 1)
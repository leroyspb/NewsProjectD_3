from celery import shared_task
import time

from django.http import HttpResponse
from django.views import View


class MyTasks(View):
    def get(self, request):
        # hello.delay()
        # printer.delay(28)

        printer.apply_async([10], countdown=5)
        hello.delay()

        return HttpResponse('Hello!')


@shared_task
def hello():
    time.sleep(2)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def digit(n, c):
    for i in range(n):
        time.sleep(c)
        print(i + 1)
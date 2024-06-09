import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_d3.settings')

app = Celery('news_d3')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_mon_8am': {
        'task': 'news.tasks.weekly_send_email_task',
        'schedule': 20,  # crontab(hour=8, minute=0, day_of_week='monday')
        'args': (20,),
    },
}

# Импортируем библиотеку  import os для взаимодействия с операционной системой и саму библиотеку Celery.
# from celery import Celery связываем настройки Django с настройками Celery через переменную окружения.
# os.environ.setdefault создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации.
# Мы также указываем пространство имен, чтобы Celery сам находил все необходимые настройки в общем конфигурационном
# файле settings.py.
# Он их будет искать по шаблону «CELERY_***».
# * Последней строчкой мы указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
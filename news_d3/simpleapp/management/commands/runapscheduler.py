import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from simpleapp.models import Product, Subscription

logger = logging.getLogger(__name__)


def my_job():

    products = Product.objects.order_by('price')[:3]
    text = '\n'.join(['{} - {}'.format(p.name, p.price) for p in products])
    mail_managers("Самые дешевые товары", text)

    # today = datetime.datetime.now()
    # last_week = today - datetime.timedelta(days=7)
    # products = Product.objects.filter(date_create_in__gte=last_week)
    # # <QuerySet [<Product: Хлеб: Хлеб Хлеб >, <Product: Кефир: Кефир Кефи>]>
    #
    # categories = list(products.values_list('category__name', flat=True))  # ['Бакалея', 'Молочная продукция']
    #
    # subscription =
    #
    # # subscription = Subscription.objects.filter(name__in=categories).values_list('subscription__email', flat=True)
    # print(subscription)
    html_content = render_to_string(
        "daily_post.html",
        {
            "link": settings.SITE_URL,
            "products": products,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статья за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=mail_managers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(),
            # (day_of_week='fri', hour=20, minute=38),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
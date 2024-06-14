from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product


class Command(BaseCommand):
    help = 'Обнуляем количество всех товаров'

    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.quantity = 0
            product.save()

            self.stdout.write(self.style.SUCCESS('Обнулили все продукты "%s"' % str(product)))
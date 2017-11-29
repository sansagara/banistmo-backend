import csv

from django.core.management import BaseCommand
from transactions.models import Transactions
from os.path import dirname, abspath, join
from datetime import datetime


class Command(BaseCommand):
    help = 'This will do an update_or_create to the Transactions model.'

    def handle(self, *args, **options):
        path = join(dirname(dirname(abspath(__file__))), 'dataset.csv')

        with open(path) as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] != 'fecha':
                    _, created = Transactions.objects.get_or_create(
                        pk=row[0],
                        date=datetime.strptime(row[1], "%Y%m%d"),
                        uuid=row[2],
                        txn=row[3])
                    if not created:
                        print('object with id {} was not created'.format(row[0]))

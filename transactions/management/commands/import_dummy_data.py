import csv
from django.core.management import BaseCommand
from transactions.models import Transaction
from os.path import dirname, abspath, join
from datetime import datetime


class Command(BaseCommand):
    help = 'This will do an update_or_create to the Transactions model.'

    def handle(self, *args, **options):
        path = join(dirname(dirname(abspath(__file__))), 'dataset.csv')

        with open(path) as file:
            reader = csv.reader(file)
            iterrow = iter(reader)
            next(iterrow)  # Skip header
            for row in iterrow:

                # Make for empty dates. I still want to insert them.
                if row[1] != '':
                    txn_date = datetime.strptime(row[1], "%Y%m%d")
                else:
                    txn_date = None

                # Make for empty dates. I still want to insert them.
                if row[3] != '':
                    txn_amount = row[3]
                else:
                    txn_amount = None

                try:
                    _, created = Transaction.objects.get_or_create(
                        pk=row[0],
                        date=txn_date,
                        uuid=row[2],
                        txn=txn_amount)
                    if not created:
                        print('Object with PK {} was not created'.format(row[0]))
                except Exception as e:
                    print('There was an exception at row {}. Exception: \n{}'.format(row[0], e))

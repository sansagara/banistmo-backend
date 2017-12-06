from django.db import models
from django.db.models import Func


class Transaction(models.Model):
    date = models.DateField()
    uuid = models.PositiveIntegerField()
    txn = models.DecimalField(max_digits=8, decimal_places=2)


class Meta:
    ordering = ['-pk']


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Day(Func):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = models.IntegerField()

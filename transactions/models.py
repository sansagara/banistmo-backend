from django.db import models


class Transaction(models.Model):
    date = models.DateField()
    uuid = models.PositiveIntegerField()
    txn = models.DecimalField(max_digits=8, decimal_places=2)


class Meta:
    ordering = ['-pk']

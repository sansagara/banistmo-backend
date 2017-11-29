from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('pk', 'date', 'uuid', 'txn')


class AvgTransactionSerializer(serializers.ModelSerializer):
    avg_txn = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('pk', 'date', 'uuid', 'txn', 'avg_txn')

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


class MonthAvgTransactionSerializer(serializers.ModelSerializer):
    avg_txn = serializers.IntegerField(read_only=True)
    sum_txn = serializers.IntegerField(read_only=True)
    month = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('month', 'sum_txn', 'avg_txn')


class DayAvgTransactionSerializer(serializers.ModelSerializer):
    avg_txn = serializers.IntegerField(read_only=True)
    sum_txn = serializers.IntegerField(read_only=True)
    day = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('day', 'sum_txn', 'avg_txn')

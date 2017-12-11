from django.db.models import Avg
from transactions.api.serializers import MonthAvgTransactionSerializer
from transactions.models import Transaction, Month


def get_txn_average():
    transactions = (Transaction.objects
                    .annotate(month=Month('date'))
                    .values('month')
                    .annotate(avg_txn=Avg('txn'))
                    .order_by('month'))
    serializer = MonthAvgTransactionSerializer(transactions, many=True)
    return serializer.data

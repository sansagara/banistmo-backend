from django.db.models import Avg
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.api.serializers import TransactionSerializer, AvgTransactionSerializer
from transactions.models import Transaction


# Generic Transactions

class TransactionList(generics.ListAPIView):
    """
     Obtención de información transaccional de los clientes que reposa en una base de datos
     y visualización gráfica de ingresos y egresos.
     Lista
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveAPIView):
    """
     Obtención de información transaccional de los clientes que reposa en una base de datos
     y visualización gráfica de ingresos y egresos.
     Detalle
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# Custom Endpoints

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_transaction_list(request, userid):
    """
    Obtiene todas las transacciones de un determinado usuario
    """
    try:
        transactions = Transaction.objects.get(uuid=userid)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def moving_average(request):
    """
    Calculo de la media móvil de 3 días del flujo de caja neto.
    """
    last_n_dates = Transaction.objects.order_by('-date').distinct('date').values_list('date', flat=True)[:3]
    transactions = Transaction.objects.filter(date__in=last_n_dates).order_by('-date')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def moving_average_grouped(request):
    """
    Calculo de la media móvil de 3 días del flujo de caja neto.
    """
    transactions = Transaction.objects.annotate(avg_txn=Avg('txn')).order_by('pk')
    serializer = AvgTransactionSerializer(transactions, many=True)
    return Response(serializer.data)

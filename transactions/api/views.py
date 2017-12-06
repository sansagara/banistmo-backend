from django.db.models import Avg
from django.http import JsonResponse
from django.conf import settings
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.api.serializers import TransactionSerializer, MonthAvgTransactionSerializer, \
    DayAvgTransactionSerializer
from transactions.models import Transaction, Month, Day
from transactions.util import get_txn_average
import django_rq


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
def moving_average_year(request, year=None):
    """
    Get the moving average for all months of dataset.
    """
    if year:
        transactions = (Transaction.objects.filter(
            date__year=year)
                        .annotate(month=Month('date'))
                        .values('month')
                        .annotate(avg_txn=Avg('txn'))
                        .order_by('month'))
    else:
        transactions = (Transaction.objects
                        .annotate(month=Month('date'))
                        .values('month')
                        .annotate(avg_txn=Avg('txn'))
                        .order_by('month'))
    serializer = MonthAvgTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def moving_average_month(request, month, year=None):
    """
    Get the moving average for all days of specified month.
    """
    if year:
        transactions = (Transaction.objects.filter(
            date__year=year, date__month=month)
                        .annotate(day=Day('date'))
                        .values('day')
                        .annotate(avg_txn=Avg('txn'))
                        .order_by('day'))
    else:
        transactions = (Transaction.objects.filter(
            date__month=month)
                        .annotate(day=Day('date'))
                        .values('day')
                        .annotate(avg_txn=Avg('txn'))
                        .order_by('day'))
    serializer = DayAvgTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def enqueue_moving_average(request):
    """
    Async calculate the moving average from last 3 months.
    This will return a url where you can poll for the result.
    """
    job = django_rq.enqueue(get_txn_average)
    polling_url = settings.BACKEND_URL + '/transactions/service2/poll/' + str(job.id)
    return JsonResponse({'url': polling_url}, status=202)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def poll_moving_average(request, job_id):
    """
    Get an async request for the moving average.
    This returns the response data on task completion.
    """
    job = django_rq.get_queue().fetch_job(job_id)
    if job:
        if job.result:
            return JsonResponse({'result': job.result, 'status': job.status}, status=200)
        else:
            return JsonResponse({'result': 'NA', 'status': job.status}, status=200)
    else:
        return JsonResponse({'id': job_id,
                             'result': 'NA',
                             'status': 'NA',
                             'help': 'Check the Django RQ admin site {} and check if the job id is there'.format(
                                 settings.DJANGO_RQ_URL)
                             }, status=202)

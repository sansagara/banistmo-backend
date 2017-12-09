from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from transactions.api import views

urlpatterns = [
    # API Documentation
    url(r'^docs/', include_docs_urls(title='Banistmo API')),

    # Endpoints for Service 1
    url(r'^service1/user/(?P<userid>\d+)$', views.user_transaction_list),
    url(r'^service1/(?P<pk>\d+)$', views.TransactionDetail.as_view()),
    url(r'^service1', views.TransactionList.as_view()),

    # Endpoints for Service 2
    url(r'^service2/poll/(?P<job_id>.+?)/?$', views.poll_moving_average),  # Poll redis for task completion
    url(r'^service2/enqueue', views.enqueue_moving_average),  # Enqueue a long-running task

    url(r'^service2/month/(?P<month>\d+)/year/(?P<year>\d+)', views.moving_average_month),  # Particular Month and Year
    url(r'^service2/month/(?P<month>\d+)', views.moving_average_month),  # Particular Month

    url(r'^service2/year/(?P<year>\d+)', views.moving_average_year),  # Particular Year
    url(r'^service2/year', views.moving_average_year),  # Default Year (2016)

    url(r'^service2', views.moving_average),
]

urlpatterns = format_suffix_patterns(urlpatterns)

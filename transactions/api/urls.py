from rest_framework.documentation import include_docs_urls
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from transactions.api import views

urlpatterns = [
    # API Documentation
    url(r'^docs/', include_docs_urls(title='Banistmo API')),

    # Endpoints
    url(r'^service1/user/(?P<userid>[0-9]+)/$', views.user_transaction_list),
    url(r'^service1/(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view()),
    url(r'^service1/', views.TransactionList.as_view()),

    url(r'^service2/grouped', views.moving_average_grouped),
    url(r'^service2/', views.moving_average),

]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.conf.urls import include, url
from django.contrib import admin
from transactions import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^transactions/', include('transactions.api.urls')),
]

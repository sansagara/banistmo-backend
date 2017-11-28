from django.contrib import admin
from .models import Transaction

# Configuration Admin
admin.site.site_header = 'BANISTMO'
admin.site.site_title = "Internal App"
admin.site.index_title = "Administration"


class AdminTransactions(admin.ModelAdmin):
    list_display = ('date', 'uuid', 'txn')

    class Meta:
        model = Transaction

admin.site.register(Transaction, AdminTransactions)

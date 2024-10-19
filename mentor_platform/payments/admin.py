# payments/admin.py

from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('mentee', 'mentor', 'session_fee', 'transaction_date', 'payment_status', 'session_date')
    search_fields = ('mentee__user__username', 'mentor__user__username', 'payment_status')
    list_filter = ('payment_status', 'session_date')

admin.site.register(Transaction, TransactionAdmin)

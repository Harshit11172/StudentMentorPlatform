from django.urls import path
from .views import DataView

urlpatterns = [
    path('universities/', DataView.as_view(), name='data_view'),
]
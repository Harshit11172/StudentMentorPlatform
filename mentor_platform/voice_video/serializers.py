# serializers.py
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['mentor', 'mentee', 'scheduled_time', 'duration', 'channel_name', 'status', 'booking_amount']

# payments/serializers.py

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # Or specify fields explicitly if needed

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.mentee = validated_data.get('mentee', instance.mentee)
        instance.mentor = validated_data.get('mentor', instance.mentor)
        instance.session_fee = validated_data.get('session_fee', instance.session_fee)
        instance.transaction_date = validated_data.get('transaction_date', instance.transaction_date)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.session_date = validated_data.get('session_date', instance.session_date)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance

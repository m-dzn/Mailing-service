from rest_framework import serializers

from app.models import Order
from .user_serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

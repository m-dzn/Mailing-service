from rest_framework import serializers

from app.models import LearningMaterial
from .order_serializers import OrderSerializer


class LearningMaterialSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = LearningMaterial
        fields = '__all__'

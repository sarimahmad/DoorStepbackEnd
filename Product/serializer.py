from rest_framework import serializers
from .models import *
from accounts.Serializers import GetUserSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class GetProductSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class AddProductSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class AddReviewSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductReview
        fields = '__all__'


class GetReviewSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    product = GetProductSerializer(read_only=True)

    class Meta:
        model = ProductReview
        fields = '__all__'


class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = '__all__'



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('order', 'status', 'created_at', 'Updated_at')


class GetPlaceOrderSerializer(serializers.ModelSerializer):
    buyer = GetUserSerializer(read_only=True)
    seller = GetUserSerializer(read_only=True)
    product = GetProductSerializer(read_only=True, many=True)
    Product_Status = StatusSerializer(many=True)

    class Meta:
        model = PlaceOrder
        fields = '__all__'

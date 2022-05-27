from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework import status


class AddProduct(APIView):
    serializers_class = AddProductSerializer

    def post(self, request):
        data = request.data
        serializers = self.serializers_class(data=data)
        if serializers.is_valid():
            serializers.save(seller=request.user)
            data = serializers.data
            responce_data = {
                'Success': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GetSellerProducts(APIView):
    def get(self, request):
        data = request.user.Seller_Products.all()
        serializers = GetProductSerializer(data, many=True)
        serializers_data = serializers.data
        return Response(serializers_data)


class GetOrdersProducts(APIView):
    def get(self, request):
        if request.user.role == "Seller":
            data = request.user.Seller_Product.all()
            serializers = GetPlaceOrderSerializer(data, many=True)
            serializers_data = serializers.data
            return Response(serializers_data)
        else:
            data = request.user.Buying_Product.all()
            serializers = GetPlaceOrderSerializer(data, many=True)
            serializers_data = serializers.data
            return Response(serializers_data)


class GetAllProduct(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request):
        All_data = Product.objects.all()
        Fruits = Product.objects.filter(category="Fruits")
        vegetables = Product.objects.filter(category="Vegetables")
        all = GetProductSerializer(All_data, many=True)
        fruits = GetProductSerializer(Fruits, many=True)
        vegetables_data = GetProductSerializer(vegetables, many=True)
        return Response({"All": all.data, "Fruits": fruits.data, "vegetables": vegetables_data.data})


class AddProductReview(APIView):
    permission_classes = [IsAuthenticated, ]
    serializers_class = AddReviewSerializer

    def post(self, request):
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            data = serializers.data
            responce_data = {
                'Success': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GetProductReview(APIView):
    def get(self, request, id):
        data = ProductReview.objects.filter(product=id)
        serializers = GetReviewSerializer(data, many=True)
        serializers_data = serializers.data
        return Response(serializers_data)


class PlaceOrderView(APIView):
    # permission_classes = [IsAuthenticated, ]
    serializers_class = PlaceOrderSerializer

    def post(self, request):
        p_id = request.data['product']
        quantity = request.data['quantity']
        try:
            product = Product.objects.get(id=p_id)
            data = product.quantity
            new_data = int(data) - int(quantity)
            print("hello",new_data)
            product.quantity = new_data
            product.save()
        except Exception as e:
            return Response("Out of Stock", status=status.HTTP_404_NOT_FOUND)
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            serializers.save(buyer=request.user)
            data = serializers.data
            responce_data = {
                'Success': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DeleteOrder(APIView):
    def delete(self, request, id):
        data = PlaceOrder.objects.get(id=id)
        data.delete()
        return Response("Order Deleted", status=status.HTTP_200_OK)


class UpdateStatus(APIView):
    serializers_class = StatusSerializer

    def post(self, request):
        if request.data['status'] == 3:
            obj = PlaceOrder.objects.get(id=request.data['order'])
            obj.delivered = True
            obj.save()
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            data = serializers.data
            responce_data = {
                "data": data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

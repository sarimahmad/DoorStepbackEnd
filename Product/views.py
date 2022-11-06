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
            data = PlaceOrder.objects.filter(seller=request.user.id)
            serializers = GetPlaceOrderSerializer(data, many=True)
            serializers_data = serializers.data
            return Response(serializers_data)
        else:
            data = PlaceOrder.objects.filter(buyer=request.user.id)
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
    permission_classes = [IsAuthenticated, ]
    serializers_class = PlaceOrderSerializer

    def post(self, request):
        p_id = request.data['product']
        quantity = request.data['quantity']
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            serializers.save(buyer=request.user)
            data = serializers.data
            for i in range(0, len(quantity)):
                product = Product.objects.get(id=p_id[i])
                new_data = int(product.quantity) - int(quantity[i])
                product.quantity = new_data
                product.save()
            responce_data = {
                'Success': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DeleteOrder(APIView):

    def delete(self, request, id):
        try:
            data = PlaceOrder.objects.get(id=id)
            product = Product.objects.get(id=data.product_id)
            quantity = request.data['quantity']
            product.quantity = product.quantity + quantity
            product.save()
            data.delete()
            return Response("Order Deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Something went Wrong", status=status.HTTP_404_NOT_FOUND)


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


class UpdateProduct(APIView):
    def post(self, request, id):
        quantity = request.data['quantity']
        try:
            product = Product.objects.get(id=id)
            product.quantity = quantity
            product.save()
            return Response({"status":1},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0}, status=status.HTTP_404_NOT_FOUND)

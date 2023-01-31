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
        # products_data = request.data['product']
        # products = []
        # all_quantity= []
        # sellers = set()
        # total_cost = 0
        # for product_data in products_data:
        #     product = Product.objects.get(pk=product_data.get('id'))
        #     quantity = product_data.get('quantity')
        #     total_cost += product.price * quantity
        #     products.append(product)
        #     all_quantity.append(quantity)
        #     sellers.add(product.seller)
        #
        # print(products)
        # print(sellers)
        # print(total_cost)
        #
        # order = PlaceOrder.objects.create(amount=total_cost)
        # order.quantity = all_quantity
        # for product in products:
        #     order.product.add(product)
        # order.seller.set(sellers)
        # order.paymentMethod = request.data['paymentMethod']
        # order_serializer = PlaceOrderSerializer(order)
        # return Response(order_serializer.data, status=status.HTTP_201_CREATED)




        p_id = request.data['product']
        quantity = request.data['quantity']
        seller = request.data['seller']
        unique_seller = list(dict.fromkeys(seller))
        order_data = {i: {"quantity": [], "product": [], "amount": []} for i in unique_seller}
        for i in range(0, len(p_id)):
            product = Product.objects.get(id=p_id[i])
            price = (product.price * quantity[i]) + 100
            order_data[seller[i]]["quantity"].append(quantity[i])
            order_data[seller[i]]["product"].append(p_id[i])
            order_data[seller[i]]["amount"].append(price)

        data = request.data
        for keys, values in order_data.items():
            data["seller"] = [keys]
            data["product"] = values["product"]
            data["quantity"] = values["quantity"]
            data["amount"] = sum(values["amount"])
            serializers = self.serializers_class(data=data)
            if serializers.is_valid():
                serializers.save(buyer=request.user)
                data = serializers.data
                for i in range(0, len(quantity)):
                    product = Product.bjects.get(id=p_id[i])
                    new_data = int(product.quantity) - int(quantity[i])
                    product.quantity = new_data
                    product.save()
            else:
                return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({
            'Success': "Order has been Place"
        }, status=status.HTTP_200_OK)


class DeleteOrder(APIView):

    def delete(self, request, id):
        try:
            quantity = request.data['quantity']
            data = PlaceOrder.objects.get(id=id)
            for index, val in enumerate(data.product.all()):
                print(val.quantity)
                new_quantity = val.quantity + int(quantity[index])
                val.quantity = new_quantity
                val.save()
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
            return Response({"status": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0}, status=status.HTTP_404_NOT_FOUND)


class EditProduct(APIView):
    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.quantity = request.data['quantity']
            product.price = request.data['price']
            product.title = request.data['title']
            print(type(request.data["image"]))
            if type(request.data["image"]) is not str:
                product.image = request.data["image"]
            product.category = request.data['category']
            product.product_description = request.data['product_description']

            product.save()
            return Response({"status": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0}, status=status.HTTP_404_NOT_FOUND)


class DeleteProduct(APIView):
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response({"status": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 0}, status=status.HTTP_404_NOT_FOUND)

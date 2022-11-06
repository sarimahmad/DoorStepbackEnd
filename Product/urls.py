from .views import *
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('AddProduct/', AddProduct.as_view(), name='Add_Product_Api'),
    path('Seller_Product/', GetSellerProducts.as_view(), name='Seller_Product_Api'),
    path('Get_Orders/', GetOrdersProducts.as_view(), name='Place_Order_Api'),
    path('get_all_Product/', GetAllProduct.as_view(), name='All_Product_Api'),
    path('Add_Review/', AddProductReview.as_view(), name='All_Product_Review_Api'),
    path('Get_Review/<int:id>/', GetProductReview.as_view(), name='All_Product_Review_Api'),
    path('PlaceOrder/', PlaceOrderView.as_view(), name='Place_Order_Api'),
    path('UpdateStatus/', UpdateStatus.as_view(), name='Place_Order_Api'),
    path('delete_order/<int:id>/', DeleteOrder.as_view(), name='All_Product_Review_Api'),
    path('UpdateQuantity/<int:id>/', UpdateProduct.as_view(), name='Update_Product_Api'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

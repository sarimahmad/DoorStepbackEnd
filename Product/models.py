from statistics import mode
from django.db import models
from django.utils import timezone


# Create your models here.


class Product(models.Model):
    Product_Type = (
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),

    )
    seller = models.ForeignKey("accounts.CustomUser", related_name="Seller_Products", on_delete=models.CASCADE,
                               default=None, blank=True, null=True)
    buyer = models.ForeignKey("accounts.CustomUser", related_name="Buyer_Products", on_delete=models.CASCADE,
                              default=None, blank=True, null=True)

    price = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="ProductImages/", null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, choices=Product_Type, null=True, blank=True)

    product_description = models.CharField(max_length=5000, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ProductReview(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE,
                             related_name="User_Review",
                             default=None, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="Product_Review",
                                default=None, blank=True, null=True)
    Review = models.CharField(max_length=1000, null=True, blank=True)


class PlaceOrder(models.Model):
    paymentMethod = (
        ("Cash", "Cash"),
        ("Credit/Debit", "Credit/Debit"),
    )
    buyer = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE,
                              related_name="Buying_Product",
                              default=None, blank=True, null=True)
    seller = models.ManyToManyField(to="accounts.CustomUser")
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = email = models.EmailField(verbose_name='email', max_length=255, blank=True, null=True,
                                      error_messages={
                                          'null': 'This feild cannot be null'})
    shipAddress = models.CharField(max_length=1000, null=True, blank=True)
    shipArea = models.CharField(max_length=1000, null=True, blank=True)
    orderNotes = models.CharField(max_length=1000, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    paymentMethod = models.CharField(max_length=100, choices=paymentMethod, null=True, blank=True)
    product = models.ManyToManyField(to=Product)
    quantity = models.JSONField(blank=True, null=True)
    amount = models.IntegerField(null=True, blank=True)


class Status(models.Model):
    order = models.ForeignKey(PlaceOrder, on_delete=models.CASCADE,
                              related_name="Product_Status",
                              default=None, blank=True, null=True)
    status = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)

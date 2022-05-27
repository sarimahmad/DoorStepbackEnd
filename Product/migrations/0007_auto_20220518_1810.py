# Generated by Django 3.2.7 on 2022-05-18 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0006_placeorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeorder',
            name='buyer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Buying_Product', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='placeorder',
            name='product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
        ),
        migrations.AlterField(
            model_name='placeorder',
            name='seller',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Seller_Product', to=settings.AUTH_USER_MODEL),
        ),
    ]
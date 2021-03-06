# Generated by Django 3.2.7 on 2022-04-23 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0003_auto_20220423_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='buyer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Buyer_Products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.CharField(blank=True, max_length=1000, null=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_Review', to='Product.product')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_Review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

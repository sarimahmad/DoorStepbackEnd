# Generated by Django 3.2.7 on 2022-05-20 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0009_placeorder_delivered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='user',
        ),
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_Status', to='Product.placeorder'),
        ),
    ]

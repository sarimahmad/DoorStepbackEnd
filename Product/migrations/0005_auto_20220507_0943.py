# Generated by Django 3.2.7 on 2022-05-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_auto_20220423_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Fruits', 'Fruits'), ('Vegetables', 'Vegetables')], max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]

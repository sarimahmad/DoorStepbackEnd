# Generated by Django 3.2.7 on 2022-11-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20221106_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='room',
            field=models.ManyToManyField(related_name='Users_Chats', to='accounts.Room'),
        ),
    ]
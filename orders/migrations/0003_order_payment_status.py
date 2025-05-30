# Generated by Django 5.2 on 2025-05-04 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_customer_name_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Not Paid', 'Not Paid'), ('Paid', 'Paid'), ('Refunded', 'Refunded'), ('Disputed', 'Disputed')], default='Not Paid', max_length=15),
        ),
    ]

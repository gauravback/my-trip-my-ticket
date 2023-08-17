# Generated by Django 4.2.4 on 2023-08-17 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelamenity',
            options={'verbose_name_plural': 'Hotel Amenities'},
        ),
        migrations.AlterModelOptions(
            name='useritinerary',
            options={'verbose_name_plural': 'User Itineraries'},
        ),
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]

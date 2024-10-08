# Generated by Django 3.2.25 on 2024-08-26 22:52

from django.db import migrations, models
import ecommerce.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_auto_20240814_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_numbers, ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='order',
            name='firstName',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_numbers, ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='order',
            name='lastName',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_numbers, ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='order',
            name='postalCode',
            field=models.CharField(max_length=6, validators=[ecommerce.validators.validate_postal_code]),
        ),
        migrations.AlterField(
            model_name='order',
            name='province',
            field=models.CharField(max_length=2, validators=[ecommerce.validators.validate_no_special_characters, ecommerce.validators.validate_no_numbers]),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_special_characters, ecommerce.validators.validate_no_numbers]),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_numbers, ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastName',
            field=models.CharField(max_length=15, validators=[ecommerce.validators.validate_no_numbers, ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.AlterField(
            model_name='user',
            name='postalCode',
            field=models.CharField(max_length=6, validators=[ecommerce.validators.validate_postal_code]),
        ),
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.CharField(max_length=2, validators=[ecommerce.validators.validate_no_special_characters, ecommerce.validators.validate_no_numbers]),
        ),
    ]

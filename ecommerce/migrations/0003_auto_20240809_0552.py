# Generated by Django 3.2.25 on 2024-08-09 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import ecommerce.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20240804_0524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('category', models.CharField(max_length=15)),
                ('available', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/images/')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=15)),
                ('lastName', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('postalCode', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=15)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paymentId', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(default='Unknown', max_length=2),
        ),
        migrations.AddField(
            model_name='user',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created'),
        ),
        migrations.AddField(
            model_name='user',
            name='firstName',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='lastName',
            field=models.CharField(default='Unknown', max_length=15),
        ),
        migrations.AddField(
            model_name='user',
            name='postalCode',
            field=models.CharField(default='Unknown', max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='province',
            field=models.CharField(default='Unknown', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(error_messages={'unique': 'A user is already registered with this nickname.'}, max_length=15, null=True, unique=True, validators=[ecommerce.validators.validate_no_special_characters]),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='ecommerce.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='ecommerce.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='ecommerce.item')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='ecommerce.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='ecommerce.item')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL),
        ),
    ]

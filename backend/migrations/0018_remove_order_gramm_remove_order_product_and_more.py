# Generated by Django 4.1.5 on 2023-01-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_subsubcategory_product_subsubcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='gramm',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='gramm',
            field=models.IntegerField(default=0),
        ),
    ]

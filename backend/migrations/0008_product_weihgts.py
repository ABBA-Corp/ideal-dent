# Generated by Django 4.1.4 on 2022-12-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_massa_delete_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weihgts',
            field=models.ManyToManyField(null=True, to='backend.massa'),
        ),
    ]
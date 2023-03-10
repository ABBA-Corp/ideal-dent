# Generated by Django 4.1.5 on 2023-01-26 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_remove_order_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(blank=True, max_length=500, null=True)),
                ('name_en', models.CharField(blank=True, max_length=500, null=True)),
                ('name_ru', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subsubcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.subsubcategory'),
        ),
    ]

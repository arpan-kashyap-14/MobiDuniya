# Generated by Django 3.0.4 on 2021-10-04 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_person_house_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='card_holder',
        ),
        migrations.RemoveField(
            model_name='person',
            name='card_no',
        ),
        migrations.RemoveField(
            model_name='person',
            name='card_type',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_seller',
        ),
        migrations.RemoveField(
            model_name='person',
            name='valid_from',
        ),
        migrations.RemoveField(
            model_name='person',
            name='valid_through',
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('samsung', 'samsung'), ('oppo', 'oppo'), ('vivo', 'vivo'), ('xiaomi', 'xiaomi'), ('realme', 'realme'), ('oneplus', 'oneplus')], max_length=10),
        ),
    ]
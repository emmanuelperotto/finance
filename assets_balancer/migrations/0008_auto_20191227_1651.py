# Generated by Django 3.0.1 on 2019-12-27 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets_balancer', '0007_auto_20191227_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='current_price_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

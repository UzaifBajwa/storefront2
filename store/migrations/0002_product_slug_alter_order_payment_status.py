# Generated by Django 4.0.6 on 2022-07-14 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'PENDING'), ('C', 'COMPLETE'), ('F', 'FAILED')], default='P', max_length=1),
        ),
    ]

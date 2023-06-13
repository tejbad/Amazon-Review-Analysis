# Generated by Django 3.1.6 on 2021-08-24 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='scrap',
        ),
        migrations.AddField(
            model_name='data',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='product',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='rating',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

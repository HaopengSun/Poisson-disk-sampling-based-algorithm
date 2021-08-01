# Generated by Django 3.1.1 on 2021-08-01 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='cellsize',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='density',
            field=models.FloatField(default=0.001631),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='finerpercent',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='minimumradius',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='algorithm',
            name='voidratio',
            field=models.FloatField(default=0.8),
        ),
    ]
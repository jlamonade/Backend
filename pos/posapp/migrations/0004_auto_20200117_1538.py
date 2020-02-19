# Generated by Django 3.0.2 on 2020-01-17 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0003_auto_20200114_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinticket',
            name='note',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='ratio',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='ratio',
            field=models.FloatField(default=1),
        ),
    ]
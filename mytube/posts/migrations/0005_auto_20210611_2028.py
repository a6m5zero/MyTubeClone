# Generated by Django 2.2 on 2021-06-11 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210611_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 2.2 on 2021-06-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255),
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

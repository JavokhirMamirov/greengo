# Generated by Django 3.2.6 on 2021-08-30 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_documents_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='type',
            field=models.IntegerField(choices=[('1', 'Documents'), ('2', 'Drivers Aplications'), ('3', 'Existiong Trucks Docs')], default=1),
        ),
    ]

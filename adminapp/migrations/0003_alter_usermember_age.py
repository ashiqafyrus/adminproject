# Generated by Django 5.0 on 2024-01-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_usermember_email_usermember_firstname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermember',
            name='age',
            field=models.IntegerField(),
        ),
    ]

# Generated by Django 5.1.3 on 2025-01-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

# Generated by Django 5.1.3 on 2025-01-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_room_tag_room_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='tags',
            field=models.ManyToManyField(related_name='rooms', to='base.tag'),
        ),
    ]
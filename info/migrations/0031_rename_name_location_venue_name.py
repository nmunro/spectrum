# Generated by Django 4.2.10 on 2024-03-07 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0030_alter_event_tags_alter_resource_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='name',
            new_name='venue_name',
        ),
    ]
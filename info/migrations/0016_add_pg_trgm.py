# Handwritten by NMunro on 2023-12-15 22:41

from django.db import migrations
import djmoney.models.fields


def create_third_party_extension(apps, schema_editor):
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def drop_third_party_extension(apps, schema_editor):
    schema_editor.execute("DROP EXTENSION IF EXISTS pg_trgm;")


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0015_alter_event_price_currency'),
    ]

    operations = [
        migrations.RunPython(create_third_party_extension, reverse_code=drop_third_party_extension, atomic=True),
    ]

# Generated by Django 4.2.8 on 2024-01-07 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0016_add_pg_trgm'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='info.organisation'),
            preserve_default=False,
        ),
    ]

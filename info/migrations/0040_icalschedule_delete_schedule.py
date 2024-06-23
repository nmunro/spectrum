# Generated by Django 4.2.13 on 2024-06-19 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0039_schedule_organisation_enable_scheduler"),
    ]

    operations = [
        migrations.CreateModel(
            name="iCalSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=255)),
                ("rrule", models.CharField(max_length=1024)),
            ],
        ),
        migrations.DeleteModel(
            name="Schedule",
        ),
    ]

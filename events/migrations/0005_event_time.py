# Generated by Django 5.0 on 2023-12-13 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0004_alter_event_end_date_alter_event_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
# Generated by Django 5.0 on 2023-12-13 06:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0003_remove_event_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_date",
            field=models.DateTimeField(),
        ),
    ]
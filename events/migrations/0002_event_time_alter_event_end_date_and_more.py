# Generated by Django 5.0 on 2023-12-13 06:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="time",
            field=models.TimeField(default="10:00"),
        ),
        migrations.AlterField(
            model_name="event",
            name="end_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_date",
            field=models.DateField(),
        ),
    ]

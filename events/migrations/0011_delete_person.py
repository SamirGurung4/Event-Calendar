# Generated by Django 5.0 on 2023-12-25 05:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0010_person"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Person",
        ),
    ]

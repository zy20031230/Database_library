# Generated by Django 5.0.6 on 2024-06-04 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("demo", "0003_delete_test"),
    ]

    operations = [
        migrations.CreateModel(
            name="Test",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="NEWTEST",
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-07 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("demo", "0007_book_image_url_alter_reservation_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
    ]

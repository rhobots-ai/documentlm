# Generated by Django 5.1.8 on 2025-05-16 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0008_remove_apilog_is_platform_alter_apiwallet_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionplan",
            name="tokens",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

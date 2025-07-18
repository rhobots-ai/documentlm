# Generated by Django 5.1.8 on 2025-04-20 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_authtoken_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="identity_provider_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="organizationmembership",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="accounts.organization",
            ),
        ),
    ]

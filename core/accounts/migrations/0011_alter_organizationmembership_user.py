# Generated by Django 5.1.8 on 2025-06-12 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_organization_logo_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationmembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memberships",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

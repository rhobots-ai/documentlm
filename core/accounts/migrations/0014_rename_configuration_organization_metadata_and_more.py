# Generated by Django 5.1.8 on 2025-06-20 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_alter_organization_configuration"),
    ]

    operations = [
        migrations.RenameField(
            model_name="organization",
            old_name="configuration",
            new_name="metadata",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="domain",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="is_white_labeled",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="logo_url",
        ),
    ]

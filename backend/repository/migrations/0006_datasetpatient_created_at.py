# Generated by Django 4.2.1 on 2023-06-06 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("repository", "0005_alter_datasetpatient_public_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasetpatient",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]

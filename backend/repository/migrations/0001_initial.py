# Generated by Django 4.2.1 on 2023-06-02 15:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("api_token", models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name="DatasetPatient",
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
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.dataset",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
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
                ("name", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="PublicID",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.organization",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "protocol_version",
                    models.CharField(choices=[("1.0.0", "1.0.0")], max_length=200),
                ),
                (
                    "first_name_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "middle_name_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "last_name_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "full_name_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "first_name_soundex_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "last_name_soundex_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "gender_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "date_of_birth_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "city_at_birth_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "address_at_bith_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "state_at_birth_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "country_at_birth_token",
                    models.CharField(
                        blank=True,
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(1024)],
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.dataset",
                    ),
                ),
                (
                    "dataset_patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.datasetpatient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GlobalPatient",
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
                (
                    "dataset_patients",
                    models.ManyToManyField(to="repository.datasetpatient"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="datasetpatient",
            name="public_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="repository.publicid"
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="repository.user"
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="repository.organization",
            ),
        ),
    ]

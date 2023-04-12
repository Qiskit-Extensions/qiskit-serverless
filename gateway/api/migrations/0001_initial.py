# Generated by Django 4.2 on 2023-04-12 12:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ComputeResource",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=100)),
                ("host", models.CharField(max_length=100)),
                ("users", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="NestedProgram",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=255)),
                ("entrypoint", models.CharField(max_length=255)),
                (
                    "artifact",
                    models.FileField(
                        upload_to="artifacts_%Y_%m_%d",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["tar"]
                            )
                        ],
                    ),
                ),
                ("arguments", models.TextField(blank=True, default="{}")),
                ("env_vars", models.TextField(blank=True, default="{}")),
                ("dependencies", models.TextField(blank=True, default="[]")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("nestedprogram"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Job",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("result", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("RUNNING", "Running"),
                            ("STOPPED", "Stopped"),
                            ("SUCCEEDED", "Succeeded"),
                            ("FAILED", "Failed"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("ray_job_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "compute_resource",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.computeresource",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.nestedprogram",
                    ),
                ),
            ],
        ),
    ]

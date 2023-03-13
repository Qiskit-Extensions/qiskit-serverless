from django.db import models
from django.conf import settings


class Program(models.Model):
    title = models.CharField(max_length=255)
    entrypoint = models.CharField(max_length=255)
    artifact = models.FileField(upload_to="artifacts_%Y_%m_%d", null=False, blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title}"


# TODO: create command to create default cluster
class ComputeResource(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    host = models.CharField(max_length=100, blank=False, null=False)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title


class Job(models.Model):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    JOB_STATUSES = [
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
        (SUCCEEDED, 'Succeeded'),
        (FAILED, 'Failed')
    ]

    program = models.ForeignKey(to=Program, on_delete=models.SET_NULL, null=True)
    result = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10,
        choices=JOB_STATUSES,
        default=PENDING,
    )
    compute_resource = models.ForeignKey(ComputeResource, on_delete=models.SET_NULL, null=True, blank=True)
    ray_job_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Job <{self.pk}> {self.program}"

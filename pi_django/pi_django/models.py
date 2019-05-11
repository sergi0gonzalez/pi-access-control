from django.db import models
from django.contrib.auth.models import User


class Permissions(models.Model):
    state = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Credential(models.Model):
    associated_name = models.CharField(max_length=70)
    status = models.CharField(max_length=70)
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.associated_name


class Log(models.Model):
    log_type = models.CharField(max_length=10)
    time_stamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.time_stamp

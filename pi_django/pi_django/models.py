from django.db import models
from django.contrib.auth.models import User


class Credential(models.Model):
    associated_name = models.CharField(max_length=70)
    status = models.CharField(max_length=70)
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.associated_name


class Log(models.Model):
    log_type = models.CharField(max_length=10)
    time_stamp = models.CharField(max_length=70)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    def __str__(self):
        return self.time_stamp

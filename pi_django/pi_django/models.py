from django.db import models
from django.contrib.auth.models import User


class UniversalUser(models.Model):
    name = models.CharField(max_length=120)
    e_mail = models.CharField(max_length=70)
    n_mec = models.IntegerField()


class Permissions(models.Model):
    start_time = models.DateField()
    end_time = models.DateField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    universal_user = models.ForeignKey(UniversalUser, on_delete=models.CASCADE, null=True)


class Credential(models.Model):
    associated_name = models.CharField(max_length=70)
    status = models.CharField(max_length=70)
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    universal_user = models.ForeignKey(UniversalUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.associated_name


class Log(models.Model):
    log_type = models.CharField(max_length=10)
    time_stamp = models.CharField(max_length=70)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    def __str__(self):
        return self.time_stamp

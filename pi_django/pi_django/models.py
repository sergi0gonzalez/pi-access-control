from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_image', blank=True)
    id_number = models.CharField(max_length=15, blank=True)
    rfid = models.CharField(max_length=12, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Permission(models.Model):
    state = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Credential(models.Model):
    status = models.CharField(max_length=70)
    data = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Method(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    status = models.BooleanField(default=False)


class Log(models.Model):
    log_type = models.CharField(max_length=10)
    time_stamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

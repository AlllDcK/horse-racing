from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Horse(models.Model):
    name = models.CharField(max_length=100)
    base_speed = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    amount = models.IntegerField()
    win_amount = models.IntegerField(default=0)
    is_win = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
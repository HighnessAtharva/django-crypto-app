import shortuuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

# This file is used to generate a referral code for each user as soon as they sign up.
def generate_referral_code():
    return shortuuid.ShortUUID().random(length=10)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, referral_code=generate_referral_code())
        profile.save()
        


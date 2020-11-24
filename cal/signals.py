from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Event, Reminder



# @receiver(pre_save, sender=Reminder)
# def create_reminder(sender, instance, created, **kwargs):
#     if created:
#         Reminder.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_reminder(sender, instance, **kwargs):
#     instance.reminder.save()



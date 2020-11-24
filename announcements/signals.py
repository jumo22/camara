from django.db.models.signals import post_save
from django.dispatch import receiver
from cal.models import Event
from ngodocs.models import NGODocument
from .models import News


@receiver(post_save, sender=Event)
def create_news_event(sender, instance, created, **kwargs):
    if created:
        News.objects.create(title=instance.title, content="event was just created!", event=instance, date_posted=instance.date_posted)


@receiver(post_save, sender=NGODocument)
def create_news_doc(sender, instance, created, **kwargs):
    if created:
        News.objects.create(title=instance.title, content="document was just added!", document=instance, date_posted=instance.date_posted)

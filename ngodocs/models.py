from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from announcements.models import Tag


class Status(models.Model):
    description = models.CharField(max_length=20)

    def __str__(self):
        return self.description


class NGODocument(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    document = models.FileField(upload_to='ngo-docs')
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})



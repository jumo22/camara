from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

from announcements.models import Tag


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(default='default.png', upload_to='events')
    date_posted = models.DateTimeField(default=timezone.now)
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    facebookurl = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        size = 300
        if img.height > size or img.width > size:
            output_size = (size, size)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def get_html_url(self):
        url = reverse('cal:event-detail', args=(self.id,))
        return f'<a href="{url}">{ self.title }</a>'

    def get_absolute_url(self):
        return reverse('cal:event-detail', kwargs={'pk': self.pk})


class Reminder(models.Model):
    reminder_date = models.DateField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Reminder no. { self.pk }'

    def save(self, **kwargs):
        super().save()

    def get_absolute_url(self):
        return reverse('cal:create-reminder')
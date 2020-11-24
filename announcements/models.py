from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        super().save()


class Announcement(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(default='default.png', upload_to='announcements')
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        # size = 250
        # if img.height > size or img.width > size:
        #     output_size = (size, size)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('announcement-detail', kwargs={'pk': self.pk})


class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    event = models.ForeignKey("cal.Event", on_delete=models.CASCADE, null=True, blank=True)
    document = models.ForeignKey("ngodocs.NGODocument", on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateTimeField()

    def __str__(self):
        return self.title

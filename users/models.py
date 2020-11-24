from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    university = models.TextField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    telephone = models.CharField(max_length=13, blank=True, null=True)
    facebookURL = models.URLField(blank=True, null=True)
    instagramURL = models.URLField(blank=True, null=True)
    linkedinURL = models.URLField(blank=True, null=True)
    twitterURL = models.URLField(blank=True, null=True)
    current_position = models.TextField(default='Volunteer')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
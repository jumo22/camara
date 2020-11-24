from django.contrib import admin
from .models import Announcement, Tag, News

admin.site.register(Tag)
admin.site.register(Announcement)
admin.site.register(News)

from django.contrib import admin
from .models import NGODocument, Status

admin.site.register(Status)
admin.site.register(NGODocument)

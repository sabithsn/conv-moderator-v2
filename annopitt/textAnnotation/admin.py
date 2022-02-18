from django.contrib import admin

# Register your models here.
from textAnnotation.models import Annotations
from textAnnotation.models import Subreddit

admin.site.register(Annotations)
admin.site.register(Subreddit)
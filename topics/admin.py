from django.contrib import admin
from .models import Topic, Answer, Upvoter, UpvoterAnswer

admin.site.register([Topic,Answer])

# Register your models here.

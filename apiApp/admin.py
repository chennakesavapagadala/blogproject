from django.contrib import admin

# Register your models here.
from postApp.models import Post

from commentApp.models import Comment

admin.site.register(Post)
admin.site.register(Comment)
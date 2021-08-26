from django.contrib import admin
from .models import Board, Topic, Post, Author, Like, Badge, Report_topic, Report_user

# Register your models here.
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Like)
admin.site.register(Badge)
admin.site.register(Report_topic)
admin.site.register(Report_user)









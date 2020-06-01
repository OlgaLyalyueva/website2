from django.contrib import admin
from .models import Post, Category, Tag, Comment, Avatar

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Avatar)

# admin.site.register(Comment)
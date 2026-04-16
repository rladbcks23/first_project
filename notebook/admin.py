from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notebook, Post, Block

admin.site.register(Notebook)
admin.site.register(Post)
admin.site.register(Block)
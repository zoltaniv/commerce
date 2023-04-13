from django.contrib import admin

from .models import Category, Auction, Comment, Rate, User

# Register your models here.
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(User)
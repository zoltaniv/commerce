from django.contrib import admin

from .models import Category, Auction, Comment, Rate, User


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "lot", "first_rate", "category_id", "user_id", "is_active" )
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "auction", "user")
    
class RateAdmin(admin.ModelAdmin):
    list_display = ("id", "current_rate", "lot_id", "user_id")
    
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name")

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(User, UserAdmin)
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        if not self.first_name or not self.last_name:
            return f"{self.username}"
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Auction(models.Model):
    lot = models.CharField(max_length=64, verbose_name="Name of product")
    description = models.TextField(verbose_name="Description of product")
    first_rate = models.IntegerField(verbose_name="Starting price")
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="catauctions", verbose_name="Product categories")
    image = models.ImageField()
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="useauctions")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.category_id}: {self.lot}"


class Comment(models.Model):
    annotation = models.TextField(verbose_name= "", max_length=264)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auccomments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usecomments")

    def __str__(self):
        return f"{self.id} {self.annotation} {self.user_id}"


class Rate(models.Model):
    current_rate = models.IntegerField(verbose_name="")
    lot_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="aucrates")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userates")

    def __str__(self):
        return f"{self.id} {self.lot_id}: {self.current_rate} {self.user_id}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usewlist")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="aucwlist")

    def __str__(self):
        return f"{self.id} {self.auction} {self.user}"

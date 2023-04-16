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
    first_rate = models.IntegerField(verbose_name="Price of product")
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories", verbose_name="Product categories")
    image = models.ImageField(upload_to='auctions/images')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.id} {self.category_id} {self.lot} {self.description} {self.first_rate}"


class Comment(models.Model):
    annotation = models.CharField(max_length=256)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="persons")

    def __str__(self):
        return f"{self.id} {self.annotation} {self.user_id}"


class Rate(models.Model):
    current_rate = models.IntegerField()
    lot_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctions")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="members")

    def __str__(self):
        return f"{self.id} {self.current_rate} {self.lot_id} {self.user_id}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="someusers")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="someauctions")

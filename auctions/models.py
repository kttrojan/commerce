from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def  __str__(self) -> str:
        return self.name


class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bid")


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image_url = models.CharField(max_length=1024)
    active = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bid_amount")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watched_listings")


    def __str__(self):
        return self.title


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f"{self.commenter} commented on '{self.listing}'."
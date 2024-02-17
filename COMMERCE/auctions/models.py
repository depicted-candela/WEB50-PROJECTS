from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):

    # Categoty's variables
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)

    # Settings for this class
    class Meta:
        ordering = ('title',)

    # Printing category object
    def __str__(self):
        return f"{self.title}"
    
    # To count the number of Auctions by category
    @property
    def count_auction(self):
        return Auction.objects.filter(category=self).count()


class Auction(models.Model):

    # Product's variables
    name = models.CharField(max_length=25)

    price = models.IntegerField()

    description = models.TextField(max_length=100)

    seller = models.ForeignKey(
        User,
        related_name="auctions",
        on_delete=models.CASCADE
        )
    
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='photos/'
        )
    
    category = models.ForeignKey(
        Category,
        null=True,
        related_name="auctions",
        on_delete=models.SET_NULL
        )
    
    start_time = models.DateTimeField()

    watchers = models.ManyToManyField(
        User,
        blank=True,
        related_name='auctions_watchers'
        )
    
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('start_time',)

    def save(self, *args, **kwargs):
        self.start_time = datetime.now()
        super().save(*args, **kwargs)

    # Printing product object
    def __str__(self):
        return f"{self.name} with a initial price of ${self.price} offered by {self.seller}"


class Bid(models.Model):

    # Bid's variables
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ('current',)

    # Printing bid object
    def __str__(self):
        if self.current:
            return f"With a value of ${self.bid}, {self.bidder} have the current bid"
        return f"With a value of ${self.bid}, {self.bidder} don't have the current bid"


class Comment(models.Model):

    # Comment's variable
    comment = models.TextField(max_length=300)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    product = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    # Printing comment object
    def __str__(self):
        return f"{self.user} commented: {self.comment}"

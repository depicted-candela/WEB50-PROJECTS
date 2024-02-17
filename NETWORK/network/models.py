from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Post(models.Model):
    
    # Post variables
    user = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE
    )
    id = models.AutoField(primary_key=True)
    posting_time = models.DateTimeField()
    text = models.TextField(max_length=240, null=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User)

    class Meta:
        ordering=('-posting_time',)
    
    def get_likes(self):
        return "\n".join([p.username for p in self.likes.all()])
    
    def save(self, *args, **kwargs):
         
        if len(args) > 0:
            self.text = args[0]
            self.image = args[1]
            super().save(force_update=True, force_insert=False, *args, **kwargs)

        else:
            self.posting_time=timezone.now()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} posted {self.text} at {self.posting_time}"

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        related_name="follows",
        on_delete=models.CASCADE
    )
    following = models.ManyToManyField(User)

    def get_following(self):
        return "\n".join([p.username for p in self.following.all()])

    def __str__(self):
        return f": follower {self.follower} follows to {self.following}" 
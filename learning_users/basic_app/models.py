from django.conf import settings
from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse

# Note: Django version is 3.1.2 and Python version is 3.8.3

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,related_name='user_info',on_delete = models.CASCADE)

    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile",kwargs={"username": self.user.username,"pk": self.pk})

class Object(models.Model):
    # user = models.OneToOneField(User,related_name='objects',on_delete = models.CASCADE, default=0)
    # user = models.ForeignKey(User, related_name="objects",on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    description = models.TextField()
    colour = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=None)
    image = models.ImageField(upload_to="objects", default=None)
    size = models.CharField(max_length=3,default=None)

    def __str__(self):
        return self.colour + " " + self.category

    def get_absolute_url(self):
        return reverse("basic_app:object_detail",kwargs={"pk":self.pk})

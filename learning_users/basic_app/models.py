from django.conf import settings
from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete = models.CASCADE)

    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)

    # additional

    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("profile",kwargs={"username": self.user.username,"pk": self.pk})



# Old code #

# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
#
# class UserProfileInfo(models.Model):
#
#     user = models.OneToOneField(User,on_delete = models.CASCADE)
#
#     # additional
#
#     portfolio_site = models.URLField(blank=True)
#
#     profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
#
#     def __str__(self):
#         return self.user.username

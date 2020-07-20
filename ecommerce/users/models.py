from django.db import models
from store.models import * 
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)


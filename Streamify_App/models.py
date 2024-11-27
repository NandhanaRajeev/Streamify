from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class registrations(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.email
    
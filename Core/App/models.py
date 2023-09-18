from django.db import models
from django.contrib.auth.models import User
from App.utils import generate_slugs

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  slug = models.SlugField(unique=True, null=True)
  
  def save(self, *args, **kwargs):
    if not self.pk:
      self.slug = generate_slugs(Profile, self.user.username)
      super(Profile, self).save(*args, **kwargs)
 
  def __str__(self) -> str:
    return f"{self.user.username} Profile"

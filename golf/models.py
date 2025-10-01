from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Golfer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"


# Add a ManyToMany field dynamically to User
User.add_to_class(
    'favorite_golfers',
    models.ManyToManyField(Golfer, blank=True, related_name='fans')
)


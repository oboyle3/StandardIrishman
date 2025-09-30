from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Golfer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"

User.add_to_class(
    'favorite_golfers',
    models.ManyToManyField(Golfer, blank=True, related_name='fans')
)

















class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_links')
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE, related_name='favored_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'golfer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.golfer.name}"
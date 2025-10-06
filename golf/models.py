from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Golfer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"

# Through model to store the rank of each golfer in the user's favorites
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'position')  # Ensures unique positions for each user

    def __str__(self):
        return f"{self.user.username}'s favorite {self.position} - {self.golfer.name}"

# Add a Many-to-Many relationship with a rank position using the through model
# User.add_to_class(
#     'favorite_golfers',
#     models.ManyToManyField(Golfer, through=UserFavorite, related_name='fans')
# )



class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class TournamentEntry(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='entries')
    golfer = models.ForeignKey(Golfer, on_delete=models.CASCADE, related_name='tournament_entries')

    # Scores per day (assuming max 4 days; you can adjust)
    day_1_score = models.IntegerField(null=True, blank=True)
    day_2_score = models.IntegerField(null=True, blank=True)
    day_3_score = models.IntegerField(null=True, blank=True)
    day_4_score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('tournament', 'golfer')  # A golfer cannot be in the same tournament twice

    def __str__(self):
        return f"{self.golfer.name} in {self.tournament.name}"
    

class Task(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveBigIntegerField()
    #order feild to order of the task

    def __str__(self):
        return self.name
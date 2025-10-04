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
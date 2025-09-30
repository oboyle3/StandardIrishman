from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Golfer
def home(request):
    return render(request, "home.html")



def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})



@login_required
def dashboard(request):
    golfers = Golfer.objects.all()                 # all available golfers
    favorites = request.user.favorite_golfers.all()  # this user’s favorites

    return render(request, 'dashboard.html', {
        'golfers': golfers,
        'favorites': favorites
    })
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
#from django.contrib.auth.decorators import login_required
from .models import Golfer
from django.contrib import messages

from django.contrib.auth.decorators import login_required
#from .models import Golfer

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



@login_required
def manage_favorites(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("favorites")

        if len(selected_ids) > 5:
            messages.error(request, "You can only select up to 5 favorite golfers.")
        else:
            golfers = Golfer.objects.filter(id__in=selected_ids)
            request.user.favorite_golfers.set(golfers)
            messages.success(request, "Your favorites were updated!")

        return redirect("manage_favorites")

    # GET → show golfers with current favorites preselected
    all_golfers = Golfer.objects.all()
    current_favorites = request.user.favorite_golfers.all()

    return render(request, "manage_favorites.html", {
        "golfers": all_golfers,
        "current_favorites": current_favorites,
    })

@login_required
def manage_favorites(request):
    all_golfers = Golfer.objects.all()

    if request.method == "POST":
        selected_ids = request.POST.getlist("favorites")

        if len(selected_ids) > 5:
            messages.error(request, "You can only select up to 5 favorite golfers.")
            return redirect("manage_favorites")

        # Update user favorites
        request.user.favorite_golfers.set(selected_ids)
        messages.success(request, "Favorites updated successfully!")
        return redirect("manage_favorites")

    # Pre-select user’s current favorites
    user_favorites = request.user.favorite_golfers.all().values_list("id", flat=True)

    return render(request, "manage_favorites.html", {
        "golfers": all_golfers,
        "user_favorites": user_favorites
    })


# @login_required
# def dashboardtest(request):
#     golfers = Golfer.objects.all()                 # all available golfers
#     favorites = request.user.favorite_golfers.all()  # this user’s favorites

#     return render(request, 'dashboard.html', {
#         'golfers': golfers,
#         'favorites': favorites
#     })

@login_required
def testpage(request):
    return render(request, "test.html")

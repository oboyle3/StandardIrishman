from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
#from django.contrib.auth.decorators import login_required
from .models import Golfer
from django.contrib import messages
from .models import Task
from django.contrib.auth.decorators import login_required
#from .models import Golfer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

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



# @login_required
# def manage_favorites(request):
#     if request.method == "POST":
#         selected_ids = request.POST.getlist("favorites")

#         if len(selected_ids) > 5:
#             messages.error(request, "You can only select up to 5 favorite golfers.")
#         else:
#             golfers = Golfer.objects.filter(id__in=selected_ids)
#             request.user.favorite_golfers.set(golfers)
#             messages.success(request, "Your favorites were updated!")

#         return redirect("manage_favorites")

#     # GET → show golfers with current favorites preselected
#     all_golfers = Golfer.objects.all()
#     current_favorites = request.user.favorite_golfers.all()

#     return render(request, "manage_favorites.html", {
#         "golfers": all_golfers,
#         "current_favorites": current_favorites,
#     })

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


@csrf_exempt
@require_POST
def update_task_order(request):
    data = json.loads(request.body)
    task_id = data['id']
    new_order = data['newOrder']

    task = Task.objects.get(id=task_id)
    task.order = new_order
    task.save()

    return JsonResponse({'success': True})
#render the tasks and implement drag and drop using javascript



@login_required
def testpage(request):
     # Fetch golfers and order them by 'order' field
    golfers = Golfer.objects.all().order_by('order')
    return render(request, 'test.html', {
        'golfers': golfers
        #'favorites': favorites
    })


def update_golfer_order(request):
    data = json.loads(request.body)
    golfer_ids = data['golfer_order']

    # Update the order of golfers
    for index, golfer_id in enumerate(golfer_ids):
        golfer = Golfer.objects.get(id=golfer_id)
        golfer.order = index  # Update golfer's order based on the new index
        golfer.save()

    return JsonResponse({'success': True})
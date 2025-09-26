from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='golf-home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),  #  dashboard URl
]

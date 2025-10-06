from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='golf-home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),  #  dashboard URl
    path("favorites/", views.manage_favorites, name="manage_favorites"),
    path("testpage/", views.testpage, name="testpage"),
    path('update-golfer-order/', views.update_golfer_order, name='update_golfer_order'),

    
]

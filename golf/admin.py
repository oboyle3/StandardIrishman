from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Golfer


# Register Golfer normally
admin.site.register(Golfer)


# Custom form for User to enforce limit
class UserChangeFormWithFavorites(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"  # include all fields

    def clean_favorite_golfers(self):
        golfers = self.cleaned_data.get("favorite_golfers")
        if golfers.count() > 5:
            raise forms.ValidationError("You can only select up to 5 favorite golfers.")
        return golfers


# Extend User admin with favorites
class UserAdmin(BaseUserAdmin):
    form = UserChangeFormWithFavorites
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Favorites", {"fields": ("favorite_golfers",)}),
    )


# Re-register User with our custom admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Golfer, UserFavorite, Tournament, TournamentEntry

# Register Golfer normally
admin.site.register(Golfer)

# Custom form for User to enforce limit on favorite golfers
class UserChangeFormWithFavorites(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"  # Include all fields

    def clean_favorite_golfers(self):
        golfers = self.cleaned_data.get("favorite_golfers")
        if golfers.count() > 5:
            raise forms.ValidationError("You can only select up to 5 favorite golfers.")
        return golfers

# Inline for UserFavorite (to manage rankings for favorite golfers)
class UserFavoriteInline(admin.TabularInline):
    model = UserFavorite
    extra = 0  # No extra empty rows
    fields = ('golfer', 'position')  # Only display the golfer and position

# Extend User admin to manage favorite golfers
class UserAdmin(BaseUserAdmin):
    form = UserChangeFormWithFavorites

    # Just append the inline for UserFavorite, no need to modify fieldsets
    inlines = [UserFavoriteInline]  # Use the inline to manage favorite golfers

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Inline for TournamentEntry
class TournamentEntryInline(admin.TabularInline):
    model = TournamentEntry
    extra = 0  # Don't show empty extra rows
    fields = ('golfer', 'day_1_score', 'day_2_score', 'day_3_score', 'day_4_score')

# Tournament Admin with inline entries
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    inlines = [TournamentEntryInline]

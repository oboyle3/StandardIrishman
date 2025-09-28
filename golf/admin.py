from django.contrib import admin
from .models import Golfer, UserFavorite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class UserFavoriteInline(admin.TabularInline):
    model = UserFavorite
    extra = 1
    raw_id_fields = ('golfer',)

class GolferAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')

# Show favorites inline on the User admin page
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserFavoriteInline,)

# unregister and re-register User admin to add the inline
from django.contrib.auth import admin as auth_admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Golfer, GolferAdmin)
admin.site.register(UserFavorite)  # optional: to manage favorites directly

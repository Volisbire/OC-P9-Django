from django.contrib import admin

# Register your models here.
from .models import Profile, Skill


admin.site.register(Skill)

class FavouritesInline(admin.TabularInline):
    model = Profile.favourites.through
    fk_name = 'from_profile'

@admin.register(Profile)
class FavouriteAdmin(admin.ModelAdmin):
    inlines = (FavouritesInline,)
    exclude = ('favourites',)
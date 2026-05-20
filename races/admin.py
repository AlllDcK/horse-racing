from django.contrib import admin
from .models import Horse, Profile, Bet

@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_speed')
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'horse', 'amount')
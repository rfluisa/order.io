from django.contrib import admin

from .models import Music, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    pass

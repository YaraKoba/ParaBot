from django.contrib import admin
from my_telebot.models import User, Cities, Spots

# Register your models here.

class SpotsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_spots')


admin.site.register(User)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Spots, SpotsAdmin)

admin.site.site_title = 'bot'
admin.site.site_header = 'bot'

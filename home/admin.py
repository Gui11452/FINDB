from django.contrib import admin
from .models import Carrossel

class CarrosselAdmin(admin.ModelAdmin):
	list_display = ('id', 'banner1', 'link1', 'banner2', 'link2', 'banner3', 'link3')
	list_per_page = 20

admin.site.register(Carrossel, CarrosselAdmin)
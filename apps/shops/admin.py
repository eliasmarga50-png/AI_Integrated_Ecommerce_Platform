

from django.contrib import admin
from .models import Shop

@admin.register(Shop)

class ShopAdmin(admin.ModelAdmin):
	
	list_display=
	list_filter=
	search_fields=
	prepopulated_fields=
	readonly_fields=
	ordering=
	
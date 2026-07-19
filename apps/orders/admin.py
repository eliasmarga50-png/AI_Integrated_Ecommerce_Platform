


from django.contrib import admin

from .models import Order, OrderItem

class OrderItemInline(models.TabularInline):
	
	model
	
	extra
	
	readonly_fields
	
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	
	list_display
	
	list_filter
	
	search_fields
	
	readonly_fields
	
	inlines
	
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	
	list_display
	
	search_fields
	
	readonly_fields



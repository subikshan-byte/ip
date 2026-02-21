from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LostItem, FoundItem

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'owner_name', 'lost_location', 'lost_date', 'created_at')
    list_filter = ('item_type', 'lost_date')
    search_fields = ('owner_name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'finder_name', 'found_location', 'found_date', 'storage_location')
    list_filter = ('item_type', 'storage_location')
    search_fields = ('finder_name', 'description')
    ordering = ('-created_at',)
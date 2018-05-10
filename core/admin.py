from __future__ import unicode_literals

from django.contrib import admin
from .models import Item, Product

class ItemModelAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ('name', 'price', 'quantity', 'unit', 'color', 'description')

admin.site.register(Item, ItemModelAdmin)
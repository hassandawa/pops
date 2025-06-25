########################################
# app\admin.py
########################################
from django import forms
from django.contrib import admin
from .models import Product, District, Market
from django.contrib import admin
from django_celery_results.models import TaskResult



class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('product', 'quantity', 'price', 'district', 'market', 'created_at')

    class Media:
        js = ('admin/js/dynamic_dropdown.js',)  # Ensure this path is correct based on your static files setup

    def save_model(self, request, obj, form, change):
        """
        Override the save_model to always create a new product entry on change.
        """
        # Remove the primary key to create a new entry
        obj.pk = None  # This ensures a new entry is created
        super().save_model(request, obj, form, change)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Market.
    """
    list_display = ('name', 'district')
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for District.
    """
    list_display = ('name',)

admin.site.register(Product, ProductAdmin)
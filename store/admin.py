from django.contrib import admin
from .models import Category, Product

# Register my models with the Django admin site using decorators.

# Register the Category model with custom admin configuration
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin
    list_display = ['name', 'slug']

    # Automatically fill in the 'slug' field based on the 'name' field
    prepopulated_fields = {'slug': ('name',)}

# Register the Product model with custom admin configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']

    # Filters to be shown in the right sidebar for quick filtering
    list_filter = ['available', 'created', 'updated']

    # Fields that can be edited directly in the list view
    list_editable = ['price', 'available']

    # Automatically fill in the 'slug' field based on the 'name' field
    prepopulated_fields = {'slug': ('name',)}

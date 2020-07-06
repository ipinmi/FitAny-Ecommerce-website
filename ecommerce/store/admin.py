from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import *
# Register your models here.

# admin views 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']

# to view the actual tree
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
# to add extra images for a product 
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category']
    list_filter = ['category']  
    inlines = [ProductImageInline]  
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
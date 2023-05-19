from django.contrib import admin
from .models import Cart, Customer, OrderPlaced, Product, Wishlist
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "slug",
        "selling_price",
        "discounted_price",
        "category",
        "brand",
        "product_image",
    ]
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "locality", "city", "state"]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "products", "quantity", "total_cost"]
    def products(self, obj):
        link = reverse("admin:online_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "customer",
        "product",
        "quantity",
        "ordered_date",
        "status",
    ]
    def products(self, obj):
        link = reverse("admin:online_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.title)
    
    def products(self, obj):
        link = reverse("admin:online_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    # def products(self, obj):
    #     link = reverse("admin:online_product_change", args=[obj.product.pk])
    #     return format_html('<a href="{}">{}</a>', link, obj.product.title)

# @admin.register(Wishlist)
# class WishlistModelAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "products"]
#     def products(self, obj):
#         link = reverse("admin:online_product_change", args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>', link, obj.product.title)


from django.contrib import admin
from .models import Order, Product, TradeEnquiry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity", "unit", "farmer_name", "location", "is_available")
    list_filter = ("category", "is_available", "location")
    search_fields = ("name", "farmer_name", "location")
    list_editable = ("price", "quantity", "is_available")


@admin.register(TradeEnquiry)
class TradeEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "enquiry_type", "product", "email", "created_at")
    list_filter = ("enquiry_type", "created_at")
    search_fields = ("name", "product", "email", "company")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "product", "quantity", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone", "product__name")
    readonly_fields = ("total_price", "created_at")

from django.contrib import admin
from .models import Order, OrderItem, OrderProgress, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderProgressInline(admin.TabularInline):
    model = OrderProgress
    extra = 0
    readonly_fields = ("status", "note", "updated_by", "created_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "full_name",
        "user",
        "customer_email",
        "amount_paid",
        "created_at",
        "shipping_address",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "id",
        "full_name",
        "email",
        "user__username",
        "user__email",
        "shipping_address__postal_code",
        "shipping_address__city",
        "shipping_address__address_line1",
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)

    inlines = (OrderItemInline, OrderProgressInline)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "email",
        "address_line1",
        "city",
        "postal_code",
        "is_default",
        "created_at",
    )
    list_filter = ("is_default", "created_at", "city")
    search_fields = (
        "full_name",
        "email",
        "address_line1",
        "address_line2",
        "city",
        "postal_code",
        "user__username",
        "user__email",
    )
    ordering = ("-is_default", "-created_at")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)

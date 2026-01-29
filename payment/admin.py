from django.contrib import admin
from .models import ShippingAddress


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "address_line1",
        "city",
        "postal_code",
        "is_default",
        "created_at",
    )

    list_filter = (
        "is_default",
        "created_at",
    )

    search_fields = (
        "full_name",
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

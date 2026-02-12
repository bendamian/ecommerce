from django.conf import settings
from django.db import models

from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.





class ShippingAddress(models.Model):
    """
    Stores UK shipping addresses for both authenticated and guest users.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shipping_addresses",
    )

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField("Email address", max_length=254, blank=True,
                              null=True,)

    address_line1 = models.CharField("Address line 1", max_length=255)
    address_line2 = models.CharField(
        "Address line 2", max_length=255, blank=True)

    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True)

    postal_code = models.CharField(
        max_length=10,
        help_text="UK postcode (e.g. SW1A 1AA)",
    )

    country = models.CharField(
        max_length=50,
        default="United Kingdom",
        editable=False,
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shipping address"
        verbose_name_plural = "Shipping addresses"
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        name = self.full_name or (self.user.username if self.user else "Guest")
        return f"{name} – {self.address_line1}, {self.city}, {self.postal_code}"


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = "created", _("Created")
        PAID = "paid", _("Paid")
        PACKING = "packing", _("Packing")
        DISPATCHED = "dispatched", _("Dispatched")
        OUT_FOR_DELIVERY = "out_for_delivery", _("Out for delivery")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField(
        _("Email address"),
        max_length=254,
        blank=True,
        null=True,
        help_text="Email used for order confirmation (guest or override).",
    )

    shipping_address = models.TextField(
        _("Shipping address"),
        blank=True,
        null=True,
        help_text="Shipping address used for order confirmation (guest or override).",
        max_length=1000,
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Total amount paid for this order.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        who = self.user.get_username() if self.user else (self.full_name or "Guest")
        return f"Order #{self.pk} — {who}"

    @property
    def customer_email(self):
        if self.email:
            return self.email
        if self.user and getattr(self.user, "email", None):
            return self.user.email
        return ""

    @property
    def is_paid(self):
        # better than amount-based logic
        return self.status in {
            self.Status.PAID,
            self.Status.PACKING,
            self.Status.DISPATCHED,
            self.Status.OUT_FOR_DELIVERY,
            self.Status.DELIVERED,
        }

    def set_status(self, new_status, note="", updated_by=None):
        if self.status == new_status:
            return

        self.status = new_status
        self.save(update_fields=["status"])


   
        from .models import OrderProgress

        OrderProgress.objects.create(
            order=self,
            status=new_status,
            note=note,
            updated_by=updated_by,
        )


    

    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        return f"Order #{self.order_id} — {self.quantity} × {product_name}"

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity
    
    @property
    def user(self):
        return self.order.user
   

class OrderProgress(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="progress",
    )

    status = models.CharField(
        max_length=30,
        choices=Order.Status.choices,
    )

    note = models.TextField(
        blank=True,
        help_text="Optional note, e.g. tracking number or courier update.",
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_progress_updates",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Order #{self.order_id} → {self.get_status_display()}"

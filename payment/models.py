from django.db import models

from django.contrib.auth.models import User

# Create your models here.


from django.conf import settings
from django.db import models


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

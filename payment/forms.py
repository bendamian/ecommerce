from django import forms
from .models import ShippingAddress

import re
from django.core.exceptions import ValidationError


import re
from django import forms
from django.core.exceptions import ValidationError
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "phone_number",
            "address_line1",
            "address_line2",
            "city",
            "county",
            "postal_code",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full name",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+44 7700 900123",
            }),
            "address_line1": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "House number and street",
            }),
            "address_line2": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apartment, suite, etc. (optional)",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City / Town",
            }),
            "county": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "County",
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "SW1A 1AA",
                "style": "text-transform: uppercase",
            }),
        }

    def clean_postal_code(self):
        postcode = self.cleaned_data["postal_code"].upper().strip()

        uk_postcode_regex = r"^(GIR ?0AA|[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})$"

        if not re.match(uk_postcode_regex, postcode):
            raise ValidationError("Enter a valid UK postcode (e.g. SW1A 1AA).")

        # Normalise spacing: "SW1A1AA" → "SW1A 1AA"
        postcode = postcode.replace(" ", "")
        return f"{postcode[:-3]} {postcode[-3:]}"

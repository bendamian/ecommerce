from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="All fields are required."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Ensure all fields are required
            field.required = True

            # Bootstrap styling
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

            # Add Bootstrap invalid class if errors exist
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already in use.")

        return email

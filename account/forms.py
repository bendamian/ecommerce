from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth import get_user_model


# User Registration Form
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



# User Login Form
class UserLoginForm(AuthenticationForm):
    """
    Custom login form extending Django's built-in AuthenticationForm.
    - Adds Bootstrap styling, placeholders, autofocus
    - Adds dynamic 'is-invalid' class for fields with errors
    - Custom error messages for better UX
    """

    # Username field with Bootstrap styling and autofocus
    username = forms.CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autofocus': True
            }
        )
    )

    # Password field with Bootstrap styling
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

    # Custom error messages
    error_messages = {
        'invalid_login': "Please enter a correct username and password.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        """
        Customize form initialization.
        Adds 'is-invalid' Bootstrap class dynamically to fields with errors.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Append 'is-invalid' class if this field has errors
            if self.errors.get(field_name):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} is-invalid'.strip()


# Profile Update Form

User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile details.
    Enforces username and email to be non-empty and email to be unique.
    """

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # current logged-in user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if not username:
            raise forms.ValidationError("Username cannot be empty.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not email:
            raise forms.ValidationError("Email address cannot be empty.")

        # Check for duplicate email (excluding current user)
        qs = User.objects.filter(email__iexact=email)

        if self.user:
            qs = qs.exclude(pk=self.user.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This email address is already in use.")

        return email




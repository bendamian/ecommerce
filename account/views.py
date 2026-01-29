from urllib import request
from django.shortcuts import redirect, render

from .forms import UserRegisterForm,UserLoginForm, ProfileUpdateForm
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
from django.views.decorators.http import require_http_methods

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .token import user_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# Create your views here.



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #form.save()
            #messages.success(request, "Account created successfully")
            #return redirect('store_app:store')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Email Verification Steps
            current_site = get_current_site(request)
            email_subject = "Activate your account" 
            email_body = render_to_string('account/registration/email-verification.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_token_generator.make_token(user),
               


            })
            user.email_user(email_subject, email_body)

            return redirect('account_app:email-verify-sent')
           

    else:
        form = UserRegisterForm()

    context={
        "form": form
    }   

    return render(request, 'account/registration/register.html', context=context)


def email_verification(request, uidb64, token):
    """
    Verify a user's email address using a UID and token.

    - Decodes the user ID from the URL
    - Checks if the token is valid
    - Activates the user account if verification succeeds
    """

    try:
        # Decode the base64 encoded user ID from the URL
        user_id = force_str(urlsafe_base64_decode(uidb64))

        # Fetch the user from the database
        user = User.objects.get(pk=user_id)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Any decoding or lookup error means verification fails
        user = None

    # Check that the user exists and the token is valid
    if user and user_token_generator.check_token(user, token):
        # Activate the user account
        user.is_active = True
        user.save(update_fields=["is_active"])

        # Redirect to success page
        return redirect('account_app:email-verify-success')

    # Token invalid or user not found
    return redirect('account_app:email-verify-failed')









def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-succes.html')

def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-faild.html')

  
def my_login(request):
    """
    Handle user login:
    - GET: Display login form
    - POST: Validate form, log in user
    - Provides Bootstrap styling for form errors dynamically
    """

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            # Get authenticated user from form
            user = form.get_user()
            login(request, user)  # Log the user in

            messages.success(request, f"Welcome, {user.username}!")
            return redirect('account_app:dashboard')  # Redirect to dashboard after login
        else:
            # Show general error if login fails
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()  # Empty form for GET request

    # Render the login page with form
    return render(request, 'account/my-login.html', {'form': form})


def my_logout(request):
    # Preserve cart if it exists
    cart = request.session.get("cart")

    # Log out the user properly
    logout(request)

    # Flush session (extra safety)
    request.session.flush()

    # Restore cart
    if cart is not None:
        request.session["cart"] = cart

    messages.success(request, "You have been logged out successfully.")
    return redirect("store_app:store")

@login_required(login_url='account_app:my-login')
def dashboard(request):
    return render(request, 'account/dashbord.html')


@login_required(login_url='account_app:my-login')
def profile_management(request):
    """
    Allow logged-in users to update their profile details.
    """
   
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST or None, instance=request.user, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile has been updated successfully."
            )
            return redirect('account_app:dashboard')

    else:
        # Load form with current user data
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'form': form
    }

    return render(
        request,
        'account/profile-management.html',
        context
    )

@login_required(login_url='account_app:my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        logout(request)  # Log out the user before deleting the account
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('store_app:store')

    return render(request, 'account/delete-account.html')


@login_required(login_url="account_app:my-login")
@require_http_methods(["GET", "POST"])
def manage_shipping_address(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user.id )


    except ShippingAddress.DoesNotExist:
        shipping_address = None
    
    form = ShippingAddressForm(instance=shipping_address)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()
            return redirect('account_app:dashboard')
    context = {
        "form": form
    }
    return render(request, 'account/manage-shipping.html', context=context)
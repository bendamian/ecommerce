from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .token import user_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
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

  
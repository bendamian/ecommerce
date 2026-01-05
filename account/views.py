from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .token import user_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# Create your views here.



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('store_app:store')
    else:
        form = UserRegisterForm()

    context={
        "form": form
    }   

    return render(request, 'account/registration/register.html', context=context)

def email_verification(request):
  pass

def email_verification_sent(request):

  pass


def email_verification_success(request):
   pass
def email_verification_failed(request):

  pass
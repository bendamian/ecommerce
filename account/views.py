from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages

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

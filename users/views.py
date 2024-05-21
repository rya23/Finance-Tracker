from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Account created for {username}")
            return redirect("login")
    else:
        form = UserRegister()

    return render(
        request,
        "users/register.html",
        {
            "form": form,
        },
    )


def login(request):
    return render(request, "users/login.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages


@login_required
def home(request):
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(
        request,
        "accounts/profile.html",
        {"form": form}
    )


@login_required
def change_password(request):
    if request.user == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "Accounts/change_password.html",
        {"form": form}
    )


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("register")  # or logout page
    return render(request, "accounts/delete_account.html")
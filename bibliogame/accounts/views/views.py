from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.conf import settings


from accounts.models import Profile
from accounts.forms import RegisterForm, ProfileUpdateForm, RegisterFormWithoutCaptcha


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already taken')
            else:
                user = form.save(commit=False)
                user.username = email
                user.set_password(form.cleaned_data['password1'])
                user.save()

                Profile.objects.create(user=user)

                login(request, user)
                messages.success(request, 'Registration successful.')
    else:
        form = RegisterForm()    

    return render(request, 'register.html', {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or "index")
        else:
            return render(request, 'login.html', {'error': 'Incorrect login or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html', {"profile": profile})


@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect('accounts:edit_profile')
    else:
        form = ProfileUpdateForm(user=user)

    return render(request, "edit_profile.html", {"form": form})


def confirm_email_view(request):
    email = request.GET.get("email")
    if not email:
        return HttpResponseBadRequest("No email provided")

    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("This email is already taken")

    form_data = request.session.get('register_form_data')
    if not form_data:
        return HttpResponseBadRequest("No registration data found")

    form_data['email'] = email

    form = RegisterFormWithoutCaptcha(form_data)
    if form.is_valid():
        user = form.save()
        login(request, user)
        del request.session['register_form_data']
        return render(request, "confirm_email.html", {"email": email})
    else:
        return HttpResponseBadRequest("Invalid form data")
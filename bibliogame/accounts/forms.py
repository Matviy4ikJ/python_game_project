from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from accounts.models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']


class RegisterFormWithoutCaptcha(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username:')
    password = forms.CharField(required=True, label='Password:', widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.user.pk if self.user else None).exists():
            raise ValidationError("This email already exists")
        return email
    

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(pk=self.user.pk if self.user else None).exists():
            raise ValidationError("This username already exists")
        return username
    

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data.get("username")
            self.user.email = self.cleaned_data.get("email")
            if commit:
                self.user.save()
                profile.user = self.user
                profile.save()
        return profile
        
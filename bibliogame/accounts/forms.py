from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
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


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(required=True, label="Email:")
    avatar = forms.ImageField(required=False, label="Upload avatar:")

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
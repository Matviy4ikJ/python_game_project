from django.urls import path

from accounts.views.views import (
    register,
    login_view,
    logout_view,
    profile_view,
    edit_profile_view,
    confirm_email_view,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', edit_profile_view, name='edit_profile_view'),
]
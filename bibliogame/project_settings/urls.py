from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include("bibliogames.urls", namespace="bibliogames")),
    path('accounts/', include("accounts.urls", namespace="accounts"))
=======
    path("captcha/", include("captcha.urls"))
>>>>>>> origin/accounts/templates
]

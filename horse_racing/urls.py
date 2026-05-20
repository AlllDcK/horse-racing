from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from races.views import race_view, deposit, withdraw
from races.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', race_view),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('register/', register, name='register')
]

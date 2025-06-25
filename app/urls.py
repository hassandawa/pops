########################################
# app\urls.py
########################################
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView  # Import LoginView here
from .views import send_otp, verify_otp, subscribe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', include('app.urls')),  # Ensure your app's URLs are included
   
]




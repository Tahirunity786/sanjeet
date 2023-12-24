from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard", dashboard, name="dashboard"),
    path("login", login_view, name="Login"),
    path("logout", logout_view, name="Logout"),
    path('about/', about, name="About"),
    path('privacy/', privacy, name="Privacy"),
    path("about_view_data/", about_view, name="About_view_data"),
    path("privacy_view_data/", privacy_view, name="privacy_view_data"),
]

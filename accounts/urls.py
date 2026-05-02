from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.user_logout, name="logout"),
    path("update-avatar/", views.update_avatar, name="update_avatar"),
]

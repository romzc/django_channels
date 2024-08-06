# chat/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),
    path("", views.RoomListView.as_view(), name="index"),
    path("<str:room_name>/", views.RoomView.as_view(), name="room"),
]
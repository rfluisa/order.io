from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="homepage-view"),
    path("internal/create", views.new_artist, name="new-artist-view"),
    path("internal/music", views.list_musics, name="list-music"),
    path("internal/detail/<int:internal_pk>/", views.music_detail, name="detail-music"),
    path("internal/login", views.LoginView.as_view(), name="login-artist"),
    path("<str:artist>", views.new_order, name="new-order"),
]

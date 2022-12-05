from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MusicForm, NewUserForm
from .models import Order, Music
from django.contrib.auth import views as auth_views
from datetime import date, timedelta


class HTTP:
    POST = "POST"
    GET = "GET"


class LoginView(auth_views.LoginView):
    template_name = "login.html"


def music_detail(request, internal_pk):
    if not request.user.is_authenticated:
        raise Http404()

    order = get_object_or_404(Order.objects.filter(artist=request.user), pk=internal_pk)
    return render(request, "music_detail.html", {"order": order})


def list_musics(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(
            artist=request.user, created_at__gte=date.today() - timedelta(days=30)
        )
        return render(request, "musics.html", {"orders": orders})
    return redirect("homepage-view")


def index(request):
    return render(request, "index.html", {"user": request.user.is_authenticated})


def new_artist(request):
    form = NewUserForm(request.POST)

    if request.method == HTTP.POST:
        if form.is_valid():
            form.save()
            return render(request, "new_artist_success.html", {"form": form})
        else:
            return render(request, "new_artist.html", {"form": form})
    return render(request, "new_artist.html", {"form": form})


def new_order(request, artist):
    try:
        artist = User.objects.get(
            username=artist, is_staff=False, is_active=True, is_superuser=False
        )
    except User.DoesNotExist:
        raise Http404()

    form = MusicForm(request.POST)

    if request.method == HTTP.GET:
        return render(
            request, "order.html", {"form": form, "username": artist.username}
        )

    if form.is_valid():
        form.save(artist=artist)
        return render(
            request, "new_success.html", {"form": form, "username": artist.username}
        )
    return render(request, "order.html", {"form": form, "username": artist.username})

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import ModelForm
from django.conf import settings

from .models import Music, Order
from .scrap import cifra_club_music_link, extract_tab_from_cifra_club


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            user.save()
            return user


class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ["title", "artist"]

    def clean_title(self):
        return self.cleaned_data["title"].capitalize()

    def clean_artist(self):
        return self.cleaned_data["artist"].capitalize()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        title = cleaned_data.get("title")
        artist = cleaned_data.get("artist")

        cifra_url = cifra_club_music_link(title, artist)
        if not cifra_url:
            self.add_error("title", "Musica não encontrada")
            return

        self.tab = extract_tab_from_cifra_club(cifra_url[0])
        self.cifra_url = cifra_url[0]
        return cleaned_data

    def save(self, artist, commit=True):
        music = super().save(commit=False)
        music.url = self.cifra_url

        with transaction.atomic():
            music.save()
            Order.objects.create(artist=artist, music=music, tab=str(self.tab))
        return

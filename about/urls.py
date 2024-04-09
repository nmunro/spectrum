from django.urls import path

from . import views

app_name = "about"

urlpatterns = [
    path("", views.AboutView.as_view(), name="about"),
    path("nmunro/", views.NMunroView.as_view(), name="nmunro"),
    path("bhosalepriyanka/", views.BhosalePriyanka.as_view(), name="bhosalepriyanka"),
]

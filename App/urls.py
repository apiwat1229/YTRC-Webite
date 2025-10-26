# App/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("contact-us/", views.contact_us, name="contact_us"),
    path("activity/<slug:slug>/", views.activity_detail, name="activity_detail"),
    # alias เก่า (optional)
    path("activity/outing/", views.activity_outing, name="activity_outing"),
    path("activity/sport-day/", views.activity_sportday, name="activity_sportday"),
]

# App/views.py
from django.shortcuts import get_object_or_404, redirect, render

from .models import Activity


def homepage(request):
    return render(request, "pages/homepage/index.html")


def contact_us(request):
    return render(request, "pages/contact-us/contactus.html")


def activity_detail(request, slug):
    act = get_object_or_404(Activity, slug=slug)
    sections = act.sections.all().prefetch_related("images")

    sections_data = []
    for sec in sections:
        images = [
            {"url": img.image.url, "alt": img.caption, "portrait": img.is_portrait}
            for img in sec.images.all()
        ]
        sections_data.append({"key": f"sec{sec.id}", "images": images})

    ctx = {"activity": act, "sections": sections, "sections_data": sections_data}
    return render(request, "pages/activity/outing_activity.html", ctx)


# alias เดิมๆ (ถ้าต้องการ)
def activity_outing(request):
    return redirect("activity_detail", slug="outing")


def activity_sportday(request):
    return redirect("activity_detail", slug="sport-day")

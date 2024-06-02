from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.decorators.http import require_http_methods
from spectrum.settings.base import DEFAULT_FROM_EMAIL, ADMIN_EMAIL_LIST

from .. import forms
from .. import models


@require_http_methods(["GET", "POST"])
def volunteer(request, org):
    org = get_object_or_404(models.Organisation, slug=org)

    if request.method == "GET":
        return render(
            request,
            "info/volunteer.html",
            {
                "org": org,
                "form": forms.VolunteerForm(initial={"organisation": org.pk}),
            },
        )

    send_mail(
        "Spectrum: New Volunteer Message",
        get_template("info/email/volunteer_org.txt").render({
            "user": request.POST["name"],
            "message": request.POST["message"],
            "email": request.POST["email"],
            "org": org,
        }),
        DEFAULT_FROM_EMAIL,
        [org.email],
        fail_silently=False,
    )

    send_mail(
        "Spectrum: Thanks for Volunteering",
        get_template("info/email/volunteer_user.txt").render({
            "user": request.POST["name"],
            "org": org,
        }),
        DEFAULT_FROM_EMAIL,
        [request.POST["email"]],
        fail_silently=False,
    )

    return redirect(org)

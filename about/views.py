from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views.generic import TemplateView


class AboutView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            return render(request, f"about/{request.GET.get('developer')}.html")

        except TemplateDoesNotExist:
            return render(request, "about/about.html")

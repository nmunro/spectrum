from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about/about.html"

class NMunroView(TemplateView):
    template_name = "about/nmunro.html"

class BhosalePriyanka(TemplateView):
    template_name = "about/bhosalepriyanka.html"

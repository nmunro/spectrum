from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramStrictWordSimilarity
from django.views.generic.base import TemplateView

from .. import forms
from .. import models

class IndexView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/index.html"

    def get(self, request):
        query = request.GET.get("search")

        if not query:
            return self.render_to_response({})

        events = models.Event.objects.annotate(
            similarity=TrigramStrictWordSimilarity(query, "name") + TrigramStrictWordSimilarity(query, "description"),
        ).filter(
            similarity__gte=0.2
        ).order_by(
            '-similarity'
        )

        resources = models.Resource.objects.annotate(
            similarity=TrigramStrictWordSimilarity(query, "name") + TrigramStrictWordSimilarity(query, "description"),
        ).filter(
            similarity__gte=0.2
        ).order_by(
            "-similarity"
        )

        return self.render_to_response({"results": [*events, *resources]})

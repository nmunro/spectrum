from pathlib import Path

from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import TrigramStrictWordSimilarity as TSWS
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic.base import TemplateView

from .. import forms
from .. import models


def favicon(request: HttpRequest) -> HttpResponse:
    file = (Path.cwd() / "static" / "images"/ "favicon.ico").open("rb")
    return FileResponse(file)

class IndexView(TemplateView):
    form_class = forms.EventForm
    template_name = "info/index.html"

    def filter_events(self, query: str):
        return models.Event.objects.annotate(
            tags_str=StringAgg("tags__name", delimiter=" "),
        ).annotate(
            similarity=TSWS(query, "event_name") + TSWS(query, "description") + TSWS(query, "tags_str"),
        ).filter(
            similarity__gte=0.01
        ).order_by(
            "-similarity"
        )

    def filter_resources(self, query: str):
        return models.Resource.objects.annotate(
            tags_str=StringAgg("tags__name", delimiter=" "),
        ).annotate(
            similarity=TSWS(query, "resource_name") + TSWS(query, "description") + TSWS(query, "tags_str"),
        ).filter(
            similarity__gte=0.01
        ).order_by(
            "-similarity"
        )

    def get(self, request):
        if query := request.GET.get("search"):
            results = [*self.filter_events(query), *self.filter_resources(query)]
            paginator = Paginator(results, 25)
            page_obj = paginator.get_page(request.GET.get("page"))

            return self.render_to_response({"page_obj": page_obj, "query": query})

        return self.render_to_response({})

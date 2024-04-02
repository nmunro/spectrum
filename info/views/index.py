from pathlib import Path

from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import TrigramStrictWordSimilarity as TSWS
from django.core.paginator import Paginator
from django.http import FileResponse, HttpRequest, HttpResponse
from django.utils import timezone
from django.views.generic.base import TemplateView

from .. import forms, models


def favicon(request: HttpRequest) -> HttpResponse:
    file = (Path.cwd() / "static" / "images" / "favicon.ico").open("rb")
    return FileResponse(file)


class IndexView(TemplateView):
    template_name = "info/index.html"
    similarity = 0.01

    def filter_events(self, query: str):
        return (
            models.Event.objects.annotate(
                tags_str=StringAgg("tags__name", delimiter=" "),
            )
            .annotate(
                similarity=TSWS(query, "event_name")
                + TSWS(query, "description")
                + TSWS(query, "tags_str"),
            )
            .filter(
                similarity__gte=self.similarity,
                start_date_time__gte=timezone.now(),
                hide=False,
            )
            .order_by("-similarity")
        )

    def filter_resources(self, query: str):
        return (
            models.Resource.objects.annotate(
                tags_str=StringAgg("tags__name", delimiter=" "),
            )
            .annotate(
                similarity=TSWS(query, "resource_name")
                + TSWS(query, "description")
                + TSWS(query, "tags_str"),
            )
            .filter(similarity__gte=self.similarity)
            .order_by("-similarity")
        )

    def get(self, request: HttpRequest) -> HttpResponse:
        if not (query := request.GET.get("search")):
            return self.render_to_response({"search_type": "all"})

        match search_type := request.GET.get("search-type"):
            case "events":
                results = self.filter_events(query)
                paginator = Paginator(results, 25)
                page_obj = paginator.get_page(request.GET.get("page"))

            case "resources":
                results = self.filter_resources(query)
                paginator = Paginator(results, 25)
                page_obj = paginator.get_page(request.GET.get("page"))

            case _:
                results = [*self.filter_events(query), *self.filter_resources(query)]
                paginator = Paginator(results, 25)
                page_obj = paginator.get_page(request.GET.get("page"))

        return self.render_to_response({
            "page_obj": page_obj,
            "query": query or "",
            "search_type": search_type,
        })

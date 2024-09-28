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


    def get(self, request: HttpRequest) -> HttpResponse:
        if not (query := request.GET.get("search")):
            return self.render_to_response({"search_type": "all"})

        results = models.Event.objects.annotate(
            tags_str=StringAgg("tags__name", delimiter=" "),
        ).annotate(
            similarity=TSWS(query, "event_name")
            + TSWS(query, "description")
            + TSWS(query, "tags_str"),
        ).filter(
            similarity__gte=self.similarity,
            start_date_time__gte=timezone.now(),
            hide=False,
        ).order_by("-similarity")

        paginator = Paginator(results, 25)
        page_obj = paginator.get_page(request.GET.get("page"))

        return self.render_to_response({"page_obj": page_obj, "query": query or ""})

from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry
from .models import Organisation, Resource, Event


@registry.register_document
class OrganisationDocument(Document):
    class Index:
        name = "organisations"
        auto_refresh = False
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Organisation
        fields = ["name", "description"]
        queryset_pagination = 5000


@registry.register_document
class ResourceDocument(Document):
    class Index:
        name = "resources"
        auto_refresh = False
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Resource
        fields = ["name", "description"]
        queryset_pagination = 5000


@registry.register_document
class ResourceDocument(Document):
    class Index:
        name = "events"
        auto_refresh = False
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Event
        fields = ["name", "description"]
        queryset_pagination = 5000

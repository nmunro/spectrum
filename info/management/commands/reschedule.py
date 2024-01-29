from django.core.management.base import BaseCommand, CommandError
from info.models import Event, Scheduler


class Command(BaseCommand):
    help = "Reschedules events"

    def handle(self, *args, **options):
        for event in Event.objects.all():
            self.stdout.write(self.style.SUCCESS(f"{event} - {event.end_date_time}"))

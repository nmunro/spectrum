from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from dateutil.rrule import rrulestr
from django.db.utils import IntegrityError

from info.models import Event, iCalSchedule, Organisation, Scheduler


class Command(BaseCommand):
    help = "Reschedules Events using iCal RRules"

    def handle(self, *args, **options):
        for schedule in iCalSchedule.objects.filter(organisation__enable_scheduler=True):
            for event in [event for event in schedule.events.all() if event.ends_today]:
                next_date = rrulestr(schedule.rrule, dtstart=event.start_date_time)[0]
                tag_names = event.tags.names()
                event.pk = None

                diff = event.end_date_time - event.start_date_time
                event.start_date_time = datetime.strptime(next_date.isoformat(), "%Y-%m-%dT%H:%M:%S%z")
                event.end_date_time = event.start_date_time + diff

                self.stdout.write(self.style.WARNING(f"Attempting to create new event '{event}'"))

                try:
                    event.save()
                    event.tags.set(tag_names)
                    event.save()
                    event.ical_rrules.add(schedule)
                    event.save()
                    self.stdout.write(self.style.SUCCESS(f"Created new event '{event}'"))

                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Failed to create new event '{event}', already exists."))


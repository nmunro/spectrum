from datetime import datetime, timedelta

from cron_converter import Cron
from django.core.management.base import BaseCommand, CommandError
import django

from info.models import Event, Scheduler


class Command(BaseCommand):
    help = "Reschedules events"

    def process_event(self, schedule, event):
        cron = Cron(schedule.cron)
        cron_schedule = cron.schedule(event.start_date_time)
        schedules = [s.id for s in event.schedules.all()]
        next_date = cron_schedule.next().isoformat()
        tag_names = event.tags.names()
        event.pk = None
        diff = event.end_date_time - event.start_date_time
        event.start_date_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        event.end_date_time = event.start_date_time + diff
        event.save()
        event.tags.set(tag_names)
        event.save()

        for pk in schedules:
            event.schedules.add(Scheduler.objects.get(pk=pk))

        event.save()
        self.stdout.write(self.style.SUCCESS(f"Creating new event '{event}' scheduled for: {next_date}"))


    def handle(self, *args, **options):
        # for each schedule, grab the events associated with it
        for schedule in Scheduler.objects.all():
            for event in [event for event in schedule.events.all() if event.ends_today]:
                try:
                    self.process_event(schedule, event)

                except django.db.utils.IntegrityError as ex:
                    self.stdout.write(self.style.SUCCESS(f"Unable to create new event '{event}': {ex}"))

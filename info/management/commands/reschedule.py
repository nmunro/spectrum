from datetime import datetime, timedelta

from cron_converter import Cron
from django.core.management.base import BaseCommand, CommandError

from info.models import Event, Scheduler


class Command(BaseCommand):
    help = "Reschedules events"

    def handle(self, *args, **options):
        # for each schedule, grab the events associated with it
        for schedule in Scheduler.objects.all():
            for event in [event for event in schedule.events.all() if event.reschedule]:
                cron = Cron(schedule.cron)
                cron_schedule = cron.schedule(event.start_date_time)
                schedules = [s.id for s in event.schedules.all()]
                # skip the first one
                next_date = cron_schedule.next().isoformat()
                event.pk = None
                diff = event.end_date_time - event.start_date_time
                event.start_date_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
                event.end_date_time = event.start_date_time + diff
                event.save()

                for pk in schedules:
                    event.schedules.add(Scheduler.objects.get(pk=pk))

                event.save()
                self.stdout.write(self.style.SUCCESS(f"Creating new event '{event}' scheduled for: {next_date}"))

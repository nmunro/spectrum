from datetime import datetime, timedelta
import time

from cron_converter import Cron
from cron_validator import CronValidator
from cron_validator.util import str_to_datetime
from django.test import TestCase

from info import models
from .factories import EventFactory, OrganisationFactory, SchedulerFactory


class SchedulerSmokeTests(TestCase):
    def setUp(self):
        self.schedule = SchedulerFactory()

    def test_default_cron_schedule(self):
        self.assertEqual("* * * * *", self.schedule.cron)

    def test_default_cron_schedule_does_match_timestamp(self):
        dt_str = time.strftime("%Y-%m-%d %H:%M")
        dt = str_to_datetime(dt_str)
        self.assertTrue(CronValidator.match_datetime("* * * * *", dt))

    def test_default_cron_schedule_does_not_match_timestamp(self):
        dt_str = f"{time.strftime('%Y-%m-%d')} 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("01 * * * *", dt))

    def test_default_cron_schedule_does_not_match_first_thursday_of_month_2024(self):
        dt_str = "2024-01-04 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_not_match_second_thursday_of_month_2024(self):
        dt_str = "2024-01-11 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_match_third_thursday_of_month_2024(self):
        dt_str = "2024-01-18 00:00"
        dt = str_to_datetime(dt_str)
        self.assertTrue(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_not_match_fourth_thursday_of_month_2024(self):
        dt_str = "2024-01-25 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_not_match_first_thursday_of_month_2023(self):
        dt_str = "2023-01-05 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_not_match_second_thursday_of_month_2023(self):
        dt_str = "2023-01-12 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_match_third_thursday_of_month_2023(self):
        dt_str = "2023-01-19 00:00"
        dt = str_to_datetime(dt_str)
        self.assertTrue(CronValidator.match_datetime("00 00 15-22 * THU", dt))

    def test_default_cron_schedule_does_not_match_fourth_thursday_of_month_2023(self):
        dt_str = "2023-01-26 00:00"
        dt = str_to_datetime(dt_str)
        self.assertFalse(CronValidator.match_datetime("00 00 15-22 * THU", dt))


class SchedulerRescheduleTests(TestCase):
    def setUp(self):
        self.test_org = OrganisationFactory(organisation_name="Test Org")

    def test_multiple_multiple_events_one_scheduler_tue(self):
        schedule = SchedulerFactory(label="Every Tuesday at 0930", cron="30 09 * * TUE")
        event = EventFactory(
            event_name="Test Event 1",
            organisation=self.test_org,
            start_date_time=str_to_datetime("2024-05-21 09:30"),
            end_date_time=str_to_datetime("2024-05-21 11:30"),
        )
        event.schedules.add(schedule)
        event.save()

        cron = Cron(schedule.cron)
        cron_schedule = cron.schedule(event.start_date_time)
        schedules = [s.id for s in event.schedules.all()]
        cron_schedule.next()
        next_date = cron_schedule.next().isoformat()
        tag_names = event.tags.names()
        event.pk = None
        diff = event.end_date_time - event.start_date_time
        new_start_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        new_end_time = event.start_date_time + diff
        event.start_date_time = new_start_time
        event.end_date_time = new_end_time
        event.save()
        event.tags.set(tag_names)
        event.save()

        for pk in schedules:
            event.schedules.add(models.Scheduler.objects.get(pk=pk))

        event.save()

        self.assertEqual(new_start_time, event.start_date_time)
        self.assertEqual(new_end_time, event.end_date_time)


    def test_multiple_multiple_events_one_scheduler_wed(self):
        schedule = SchedulerFactory(label="Every Wednesday at 0930", cron="30 09 * * WED")
        event = EventFactory(
            event_name="Test Event 2",
            organisation=self.test_org,
            start_date_time=str_to_datetime("2024-05-22 09:30"),
            end_date_time=str_to_datetime("2024-05-22 11:30"),
        )
        event.schedules.add(schedule)
        event.save()

        cron = Cron(schedule.cron)
        cron_schedule = cron.schedule(event.start_date_time)
        schedules = [s.id for s in event.schedules.all()]
        cron_schedule.next()
        next_date = cron_schedule.next().isoformat()
        tag_names = event.tags.names()
        event.pk = None
        diff = event.end_date_time - event.start_date_time
        new_start_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        new_end_time = event.start_date_time + diff
        event.start_date_time = new_start_time
        event.end_date_time = new_end_time
        event.save()
        event.tags.set(tag_names)
        event.save()

        for pk in schedules:
            event.schedules.add(models.Scheduler.objects.get(pk=pk))

        event.save()

        self.assertEqual(new_start_time, event.start_date_time)
        self.assertEqual(new_end_time, event.end_date_time)


    def test_multiple_multiple_events_one_scheduler_thu(self):
        schedule = SchedulerFactory(label="Every Thursday at 0930", cron="30 09 * * THU")
        event = EventFactory(
            event_name="Test Event 3",
            organisation=self.test_org,
            start_date_time=str_to_datetime("2024-05-23 09:30"),
            end_date_time=str_to_datetime("2024-05-23 11:30"),
        )
        event.schedules.add(schedule)
        event.save()

        cron = Cron(schedule.cron)
        cron_schedule = cron.schedule(event.start_date_time)
        schedules = [s.id for s in event.schedules.all()]
        cron_schedule.next()
        next_date = cron_schedule.next().isoformat()
        tag_names = event.tags.names()
        event.pk = None
        diff = event.end_date_time - event.start_date_time
        new_start_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        new_end_time = event.start_date_time + diff
        event.start_date_time = new_start_time
        event.end_date_time = new_end_time
        event.save()
        event.tags.set(tag_names)
        event.save()

        for pk in schedules:
            event.schedules.add(models.Scheduler.objects.get(pk=pk))

        event.save()

        self.assertEqual(new_start_time, event.start_date_time)
        self.assertEqual(new_end_time, event.end_date_time)


    def test_multiple_multiple_events_one_scheduler_fri(self):
        schedule = SchedulerFactory(label="Every Friday at 0930", cron="30 09 * * FRI")
        event = EventFactory(
            event_name="Test Event 4",
            organisation=self.test_org,
            start_date_time=str_to_datetime("2024-05-24 09:30"),
            end_date_time=str_to_datetime("2024-05-24 11:30"),
        )
        event.schedules.add(schedule)
        event.save()

        cron = Cron(schedule.cron)
        cron_schedule = cron.schedule(event.start_date_time)
        schedules = [s.id for s in event.schedules.all()]
        cron_schedule.next()
        next_date = cron_schedule.next().isoformat()
        tag_names = event.tags.names()
        event.pk = None
        diff = event.end_date_time - event.start_date_time
        new_start_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        new_end_time = event.start_date_time + diff
        event.start_date_time = new_start_time
        event.end_date_time = new_end_time
        event.save()
        event.tags.set(tag_names)
        event.save()

        for pk in schedules:
            event.schedules.add(models.Scheduler.objects.get(pk=pk))

        event.save()

        self.assertEqual(new_start_time, event.start_date_time)
        self.assertEqual(new_end_time, event.end_date_time)


    def test_multiple_events_and_schedules(self):
        schedule_1 = SchedulerFactory(label="Every Friday at 0930", cron="30 09 * * FRI")
        event_1 = EventFactory(
            event_name="Test Event 1",
            organisation=self.test_org,
            start_date_time=str_to_datetime("2024-05-24 09:30"),
            end_date_time=str_to_datetime("2024-05-24 11:30"),
        )
        event_1.schedules.add(schedule_1)
        event_1.save()

        cron = Cron(schedule_1.cron)
        cron_schedule = cron.schedule(event_1.start_date_time)
        schedules = [s.id for s in event_1.schedules.all()]
        tag_names = event_1.tags.names()
        diff = event_1.end_date_time - event_1.start_date_time
        event_1.pk = None

        next_date = cron_schedule.next().isoformat()

        if datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z") == event_1.start_date_time:
            next_date = cron_schedule.next().isoformat()

        new_start_time = datetime.strptime(next_date, "%Y-%m-%dT%H:%M:%S%z")
        new_end_time = new_start_time + diff
        event_1.start_date_time = new_start_time
        event_1.end_date_time = new_end_time
        event_1.save()
        event_1.tags.set(tag_names)
        event_1.save()

        for pk in schedules:
            event_1.schedules.add(models.Scheduler.objects.get(pk=pk))

        event_1.save()

        self.assertEqual(event_1.start_date_time.isoformat(), "2024-05-31T09:30:00+00:00")
        self.assertEqual(event_1.end_date_time.isoformat(), "2024-05-31T11:30:00+00:00")

import time

from cron_validator import CronValidator
from cron_validator.util import str_to_datetime
from django.test import TestCase
from info import models
from .factories import SchedulerFactory


class SchedulerTests(TestCase):
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

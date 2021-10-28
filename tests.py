from unittest import TestCase
from constraint import *
from datetime import datetime, timedelta, date, time

class ConstraintTester(TestCase):
    def test_every_sun_sat(self):

        basis = datetime(2012, 10, 15).date()
        con = RepetitiveConstraint(ConstraintUnion([DayOfWeekConstraint(5), DayOfWeekConstraint(6)]), RepetitiveType.WEEKLY, 1, basis)

        i = timedelta(seconds=1)

        today = datetime(2012, 12, 25, 12, 0)
        self.assertFalse(con.check(today, today + i))
        today = datetime(2012, 12, 26, 12, 0)
        self.assertFalse(con.check(today, today + i))
        today = datetime(2012, 12, 27, 12, 0)
        self.assertFalse(con.check(today, today + i))
        today = datetime(2012, 12, 28, 12, 0)
        self.assertFalse(con.check(today, today + i))
        today = datetime(2012, 12, 29, 12, 0)
        self.assertTrue(con.check(today, today + i))
        today = datetime(2012, 12, 30, 12, 0)
        self.assertTrue(con.check(today, today + i))
        today = datetime(2012, 12, 31, 12, 0)
        self.assertFalse(con.check(today, today + i))
        today = datetime(2013, 1, 1, 12, 0)
        self.assertFalse(con.check(today, today + i))

    def test_every_other_month_sun_sat(self):

        basis = datetime(2012, 10, 15).date()
        every_sat_sun = RepetitiveConstraint(ConstraintUnion([DayOfWeekConstraint(5), DayOfWeekConstraint(6)]), RepetitiveType.WEEKLY, 1, basis)
        every_other_month_sun_sat = RepetitiveConstraint(every_sat_sun, RepetitiveType.MONTHLY, 2, basis)

        i = timedelta(seconds=1)
        today = datetime(2012, 12, 25, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 26, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 27, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 28, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 29, 12, 0)
        self.assertTrue(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 30, 12, 0)
        self.assertTrue(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 12, 31, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2013, 1, 1, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))

        today = datetime(2012, 11, 23, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 24, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 25, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 26, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 27, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 28, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 29, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))
        today = datetime(2012, 11, 30, 12, 0)
        self.assertFalse(every_other_month_sun_sat.check(today, today + i))

    def test_every_day_8_846am(self):
        # basis = datetime(2001, 9, 11).date()
        eight = time(8, 0)
        eight46 = time(8, 46)
        _8_840am = TimeOfDayConstraint(eight, eight46)

        tower_fall = datetime(2001, 9, 11, 8, 46, 40)
        i = timedelta(seconds=1)

        self.assertFalse(_8_840am.check(tower_fall - timedelta(hours=1), tower_fall - timedelta(hours=1) + i))  # 7:46
        self.assertFalse(_8_840am.check(tower_fall - timedelta(minutes=47), tower_fall - timedelta(minutes=47) + i))  # 7:59
        self.assertEqual(1.0, _8_840am.check(tower_fall - timedelta(minutes=46), tower_fall - timedelta(minutes=46) + i))  # 8:00
        self.assertEqual(1.0, _8_840am.check(tower_fall - timedelta(minutes=20), tower_fall - timedelta(minutes=20) + i))  # 8:26
        self.assertFalse(_8_840am.check(tower_fall, tower_fall + i))  # 8:46
        self.assertFalse(_8_840am.check(tower_fall + timedelta(hours=1), tower_fall + timedelta(hours=1) + i))
        self.assertFalse(_8_840am.check(tower_fall + timedelta(hours=11, minutes=30), tower_fall + timedelta(hours=11, minutes=30) + i))  # 8:16pm
        self.assertFalse(_8_840am.check(tower_fall + timedelta(days=1), tower_fall + timedelta(days=1) + i))
        self.assertEqual(1.0, _8_840am.check(tower_fall + timedelta(days=1) - timedelta(minutes=7), tower_fall + timedelta(days=1) - timedelta(minutes=7) + i))  # 8:45
        self.assertGreater(_8_840am.check(tower_fall - timedelta(minutes=20), tower_fall), 0.0)  # 8:26-8:46
        self.assertEqual(1.0, _8_840am.check(tower_fall - timedelta(minutes=20), tower_fall - timedelta(minutes=10)))  # 8:26-8:36
        self.assertGreater(_8_840am.check(tower_fall - timedelta(hours=1), tower_fall - timedelta(minutes=10)), 0.0)  # 7:46-8:36

    def test_every_third_month_sun_4pm_5pm_sat_3am_5am(self):
        basis = datetime(2012, 1, 15).date()

        pm4 = time(16)
        pm5 = time(17)

        am3 = time(3)
        am5 = time(5)

        sun_pm4to5 = ConstraintIntersect([DayOfWeekConstraint(6), TimeOfDayConstraint(pm4, pm5)])
        sat_am3to5 = ConstraintIntersect([DayOfWeekConstraint(5), TimeOfDayConstraint(am3, am5)])

        third_month = RepetitiveConstraint(ConstraintUnion([sun_pm4to5, sat_am3to5]), RepetitiveType.MONTHLY, 3, basis)

        i = timedelta(seconds=1)
        def test(mo, da, h, result):
            dt = datetime(2012, mo, da, h)
            self.assertEqual(result, third_month.check(dt, dt + i), str(dt))

        for m in [1,4,7]:
            test(m, 21, 3, True)
        for m in [2,3,5,6,8,9,10,11,12]:
            test(m, 21, 3, False)

        for m in [1,4,7]:
            test(m, 22, 16, True)
        for m in [2,3,5,6,8,9,10,11,12]:
            test(m, 22, 16, False)

        true = [7,14,21,28]
        for d in true:
            test(4, d, 3, True)
        for d in set(range(1,31)).difference(true):
            test(4, d, 3, False)

    def test_overnight_event(self):
        # first day of every month at noon to the second day of the month at noon

        sleep_over_time_start = datetime(2000, 1, 1, 18)
        sleep_over_time_end = datetime(2000, 1, 3, 6)

        first_day_of_month = DayOfMonthConstraint(1)
        second_day_of_month = DayOfMonthConstraint(2)
        third_day_of_month = DayOfMonthConstraint(3)

        noon_to_midnight = TimeOfDayConstraint(time(12), time.max)
        mid_to_mid = TimeOfDayConstraint(time.min, time.max)
        midnight_to_noon = TimeOfDayConstraint(time.min, time(12))

        first_and_second_day_with_time = DateConstraint(sleep_over_time_start - timedelta(days=1), sleep_over_time_end)

        #first_and_second_day_with_time = ConstraintIntersect([first_day_of_month, noon_to_midnight])
        x = first_and_second_day_with_time._check(sleep_over_time_start, sleep_over_time_end)
        self.assertAlmostEqual(1.0, first_and_second_day_with_time.check(sleep_over_time_start, sleep_over_time_end))
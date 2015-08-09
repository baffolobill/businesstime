import datetime

from business import Business
from day import Day
from days import Days
from datetime_period import DateTimePeriod
from util import next_weekday

# Opening hours for each week day. If not specified, it is considered closed
days = [
    # Standard days with fixed opening hours
    Day(Days.MONDAY, [['09:00', '14:00'], ['14:45', '18:00']]),
    Day(Days.TUESDAY, [['09:00', '14:00'], ['14:45', '18:00']]),
    Day(Days.WEDNESDAY, [['09:00', '14:00'], ['14:45', '18:00']]),
    Day(Days.THURSDAY, [['09:00', '14:00'], ['14:45', '18:00']]),
    Day(Days.FRIDAY, [['09:00', '14:00'], ['14:45', '16:45']]),
    Day(Days.SATURDAY, [['09:00', '10:00'], ['11:00', '12:00'], ['13:00', '14:00'], ['15:00', '16:45']]),
]


# Create a new Business instance
business = Business(days)

if False:
    nextDate = business.closest(datetime.datetime(2015, 5, 11, 10, 0))
    print nextDate

if False:
    start = datetime.datetime(2015, 5, 11, 10, 0)
    end = datetime.datetime(2015, 5, 14, 10, 0)

    dates = business.timeline(start, end, interval=1);
    print dates

#
# datetime.datetime(2015, 8, 7) == Friday
# Both values in the same day

# both values in the same interval
case1 = business.timedelta(datetime.datetime(2015, 8, 7, 12), datetime.datetime(2015, 8, 7, 12, 10))
print(case1) # 10 minutes + 0 minutes
# start_time in first interval, end_time in last_interval
case2 = business.timedelta(datetime.datetime(2015, 8, 7, 12), datetime.datetime(2015, 8, 7, 15, 10))
print(case2) # 2 hours + 25 minutes
# start_time equals first interval start, end_time equals last_interval end
case3 = business.timedelta(datetime.datetime(2015, 8, 7, 9), datetime.datetime(2015, 8, 7, 16, 45))
print(case3) # 5 hours + 2 hours
# both values in last interval
case4 = business.timedelta(datetime.datetime(2015, 8, 7, 14, 45), datetime.datetime(2015, 8, 7, 16, 45))
print(case4) # 0 hours + 2 hours
# start_time before first interval, end_time in first interval
case5 = business.timedelta(datetime.datetime(2015, 8, 7, 8, 0), datetime.datetime(2015, 8, 7, 9, 10))
print(case5) # 10 minutes
# start_time before first interval, end_time after first interval
case6 = business.timedelta(datetime.datetime(2015, 8, 7, 8, 0), datetime.datetime(2015, 8, 7, 14, 10))
print(case6) # 5 hours + 0 hours
# start_time before first interval, end_time after last interval
case7 = business.timedelta(datetime.datetime(2015, 8, 7, 8, 0), datetime.datetime(2015, 8, 7, 18, 10))
print(case7) # 5 hours + 2 hours
# start_time before first interval, end_time in last interval
case8 = business.timedelta(datetime.datetime(2015, 8, 7, 8, 0), datetime.datetime(2015, 8, 7, 14, 50))
print(case8) # 5 hours + 5 minutes
# both values after last interval
case9 = business.timedelta(datetime.datetime(2015, 8, 7, 18, 0), datetime.datetime(2015, 8, 7, 18, 50))
print(case9) # 0 hours + 0 hours
# both values between intervals
case10 = business.timedelta(datetime.datetime(2015, 8, 7, 14, 0), datetime.datetime(2015, 8, 7, 14, 45))
print(case10) # 0 hours + 0 hours
# start_time in first interval, end_time after first_interval
case11 = business.timedelta(datetime.datetime(2015, 8, 7, 12, 0), datetime.datetime(2015, 8, 7, 14, 45))
print(case11) # 2 hours + 0 hours

#
# datetime.datetime(2015, 8, 8) == Saturday
# Both values in the same day

# start_time in first_interval, end_time in last_interval
case2_1 = business.timedelta(datetime.datetime(2015, 8, 8, 9), datetime.datetime(2015, 8, 8, 16))
print(case2_1) # 1 hour + 1 hour + 1 hour + 1 hour


#
# Both values in the different days
#

print('= Several days =')
# start_time in first_interval, end_time in last_interval
case3_1 = business.timedelta(datetime.datetime(2015, 8, 7, 9), datetime.datetime(2015, 8, 8, 16))
print(case3_1) # day 1: 5 hours + 2 hours; day 2: 1 hour + 1 hour + 1 hour + 1 hour; Total: 11 hours

case3_2 = business.timedelta(datetime.datetime(2015, 8, 6, 14), datetime.datetime(2015, 8, 7, 9))
print(case3_2) # day 1: 3:15; day 2: 0 minutes; Total: 3 hours 15 minutes

case3_3 = business.timedelta(datetime.datetime(2015, 8, 6, 14), datetime.datetime(2015, 8, 8, 10))
print(case3_3) # day 1: 3:15; day 2: 7 hours; day 3: 1 hour Total: 11 hours 15 minutes

case3_4 = business.timedelta(datetime.datetime(2015, 8, 6, 9), datetime.datetime(2015, 8, 8, 10))
print(case3_4) # day 1: 8:15; day 2: 7 hours; day 3: 1 hour Total: 16 hours 15 minutes

case3_5 = business.timedelta(datetime.datetime(2015, 8, 6, 8), datetime.datetime(2015, 8, 8, 10))
print(case3_5) # day 1: 8:15; day 2: 7 hours; day 3: 1 hour Total: 16 hours 15 minutes

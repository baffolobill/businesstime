import datetime


def next_weekday(d, isoweekday):
    days_ahead = isoweekday - d.isoweekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def prev_weekday(d, isoweekday):
    """
    d=1 isoweekday=1 days_behind=7
    d=1 isoweekday=2 days_behind=6
    d=1 isoweekday=7 days_behind=1
    """
    days_behind = 7 + d.isoweekday() - isoweekday
    return d - datetime.timedelta(days_behind)

from datetime import datetime, timedelta
import math

def julian_date(dt):

    dt_utc = dt - timedelta(hours=5, minutes=30)
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)

    JD = (math.floor(365.25 * (year + 4716)) +
          math.floor(30.6001 * (month + 1)) +
          day + B - 1524.5 +
          (hour + minute / 60 + second / 3600) / 24)

    return JD

def days_in_month(year, month):

    if month == 2:
        # Leap year check
        return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def compute_lst(ist_dt, longitude=72.7761):
    
    # Step 1: Convert IST to UT
    ut_dt = ist_dt - timedelta(hours=5, minutes=30)
    ut_hours = ut_dt.hour + ut_dt.minute / 60 + ut_dt.second / 3600
    
    # Step 2: Calculate days since J2000.0
    JD = julian_date(ist_dt)
    D = JD - 2451545.0
    
    # Step 3: Compute GMST
    GMST = (18.697374558 + 24.06570982441908 * D) % 24
    
    # Step 4: Convert GMST to LST
    LST = (GMST + (longitude / 15)) % 24
    

    LST_year = ut_dt.year
    LST_month = ut_dt.month
    LST_day = ut_dt.day

    if LST < 0:
        LST_day -= 1  # Move back one day
        if LST_day == 0:  # Handle month change
            LST_month -= 1
            if LST_month == 0:  # Handle year change
                LST_month = 12
                LST_year -= 1
            LST_day = days_in_month(LST_year, LST_month)

    total_seconds = LST * 3600
    LST_hour = int(total_seconds // 3600)
    LST_minute = int((total_seconds % 3600) // 60)
    LST_second = int(round(total_seconds % 60))

    # Ensure LST_second does not exceed 59
    if LST_second == 60:
        LST_second = 0
        LST_minute += 1

    # Ensure LST_minute does not exceed 59
    if LST_minute == 60:
        LST_minute = 0
        LST_hour += 1
    
    if LST_hour == 24:
        LST_hour = 0
        ut_dt += timedelta(days=1)

    ls_dt = datetime(LST_year, LST_month, LST_day, LST_hour, LST_minute, LST_second)
    return ls_dt

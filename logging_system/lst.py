"""
Local Sidereal Time (LST) Calculator.

This module provides functions to:
- Convert a datetime to Julian Date.
- Calculate the number of days in a given month.
- Convert IST to Local Sidereal Time for a given longitude (default: Mt. Abu).

Sidereal Time is used in astronomy to track celestial objects. It differs from solar time.
"""

from datetime import datetime, timedelta
import math

def julian_date(dt):

    """
    Convert a datetime object (IST) to Julian Date.

    Args:
        dt (datetime): Datetime in IST.

    Returns:
        float: Julian Date value adjusted to UTC.
    """

    dt_utc = dt - timedelta(hours=5, minutes=30) # Convert IST to UTC
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour
    minute = dt_utc.minute
    second = dt_utc.second

    # January and February adjustment
    if month <= 2:
        year -= 1
        month += 12

    # Julian calendar to Gregorian calendar correction
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)

    # Final Julian Date computation
    JD = (math.floor(365.25 * (year + 4716)) +
          math.floor(30.6001 * (month + 1)) +
          day + B - 1524.5 +
          (hour + minute / 60 + second / 3600) / 24)

    return JD

def days_in_month(year, month):
    """
    Return the number of days in a given month and year.
    Handles leap years.

    Args:
        year (int): Year
        month (int): Month (1-12)

    Returns:
        int: Number of days
    """

    if month == 2:
        # Leap year check
        return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def compute_lst(ist_dt, longitude=72.7761):
    """
    Compute Local Sidereal Time (LST) from IST.

    Steps:
    1. Convert IST to UTC.
    2. Calculate Julian Date.
    3. Compute number of days since J2000.0.
    4. Calculate GMST using astronomical formula.
    5. Adjust GMST with local longitude to get LST.
    6. Handle edge cases (LST overflows, day wrap-around).

    Args:
        ist_dt (datetime): Datetime in IST.
        longitude (float): Longitude in degrees (default: Mt. Abu - 72.7761° E).

    Returns:
        datetime: Corresponding LST datetime object.
    """
    
    # Step 1: Convert IST to UT
    ut_dt = ist_dt - timedelta(hours=5, minutes=30)
    ut_hours = ut_dt.hour + ut_dt.minute / 60 + ut_dt.second / 3600
    
    # Step 2: Calculate days since J2000.0
    JD = julian_date(ist_dt)
    D = JD - 2451545.0  # J2000.0 reference

    
    # Step 3: Compute GMST
    GMST = (18.697374558 + 24.06570982441908 * D) % 24
    
    # Step 4: Convert GMST to LST
    LST = (GMST + (longitude / 15)) % 24
    

    # Prepare LST date parts
    LST_year = ut_dt.year
    LST_month = ut_dt.month
    LST_day = ut_dt.day


    # Handle negative LST edge case
    if LST < 0:
        LST_day -= 1  # Move back one day
        if LST_day == 0:  # Handle month change
            LST_month -= 1
            if LST_month == 0:  # Handle year change
                LST_month = 12
                LST_year -= 1
            LST_day = days_in_month(LST_year, LST_month)


    # Convert LST hours to time components
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

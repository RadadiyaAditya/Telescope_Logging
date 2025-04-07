from astropy.time import Time
import astropy.units as u
from astropy.coordinates import EarthLocation
import datetime

# Mount Abu Location
mt_abu_location = EarthLocation(lat=24.5926, lon=72.7156, height=1700)

def compute_lst(utc_dt=None):
    """
    Compute Local Sidereal Time (LST) at Mount Abu for the given UTC datetime.

    Args:
        utc_dt (datetime.datetime, optional): UTC datetime. Defaults to current UTC time.

    Returns:
        str: Local Sidereal Time as HH:MM:SS string
    """
    if utc_dt is None:
        utc_dt = datetime.datetime.utcnow()

    time = Time(utc_dt, scale='utc', location=mt_abu_location)
    lst = time.sidereal_time('mean', longitude=mt_abu_location.lon)

    total_seconds = lst.hour * 3600
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    formatted_lst = f"{utc_dt.date()} {hours:02d}:{minutes:02d}:{seconds:02d}"
    return formatted_lst

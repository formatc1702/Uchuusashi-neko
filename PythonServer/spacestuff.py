import ephem
import datetime
import urllib.request


def get_alt_az_from_tle(tle, loc_str):
    loc = ephem.city(loc_str)
    obj = calc_obj_from_tle(tle, loc)
    return obj.alt, obj.az

def get_next_pass_from_tle(tle, loc_str):
    loc = ephem.city(loc_str)
    obj = calc_obj_from_tle(tle, loc)
    rise_time, rise_az, max_time, max_alt, set_time, set_az = loc.next_pass(obj)
    rise_time = rise_time.datetime().replace(microsecond=0)
    max_time  = max_time.datetime().replace(microsecond=0)
    set_time  = set_time.datetime().replace(microsecond=0)
    return rise_time, rise_az, max_time, max_alt, set_time, set_az

def calc_obj_from_tle(tle, loc):
    loc.date = datetime.datetime.utcnow()
    obj = ephem.readtle(tle[0], tle[1], tle[2])
    obj.compute(loc)
    return obj

def get_tle_from_url(url, obj):
    src = iter(urllib.request.urlopen(url))
    for line_raw in src:
        line = line_raw.decode("utf-8")
        if obj in line:
            tle0 = line.strip()
            tle1 = next(src).decode("utf-8").strip()
            tle2 = next(src).decode("utf-8").strip()
            return tle0, tle1, tle2

def compass_heading(ang_deg, pts=8):
    if  pts == 4:
        dirs = ['N','E','S','W']
    elif pts == 8:
        dirs = ['N','NE','E','SE','S','SW','W','NW']
    elif pts == 16:
        dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
    idx = int(round(ang_deg / 360.0 * len(dirs), 0))
    idx %= len(dirs)
    return dirs[idx]

#!/usr/bin/env python3
import spacestuff
from math import degrees

loc      = 'Berlin'
tle_src  = 'https://www.celestrak.com/NORAD/elements/stations.txt'
tle_name = 'ISS (ZARYA)'

# sample TLE (do not use):
# tle0 = 'ISS (ZARYA)'
# tle1 = '1 25544U 98067A   17073.59757234  .00003182  00000-0  55149-4 0  9992'
# tle2 = '2 25544  51.6435 149.8114 0007006 291.5980 211.5204 15.54208770 47040'

print('Location of {} from {}:'.format(tle_name, loc))

tle = spacestuff.get_tle_from_url(tle_src, tle_name)

print(tle[0])
print(tle[1])
print(tle[2])

alt, az = spacestuff.get_alt_az_from_tle(tle, loc)
alt = round(degrees(alt), 2)
az  = round(degrees(az),  2)
heading = spacestuff.compass_heading(az, 16)

print('Alt: {}\nAz: {} ({})'.format(alt, az, heading))

print('')

print('Next pass over {}:'.format(loc))

rise_time, rise_az, max_time, max_alt, set_time, set_az, visible = spacestuff.get_next_pass_from_tle(tle, loc)

rise_az = round(degrees(rise_az), 2)
max_alt = round(degrees(max_alt), 2)
set_az  = round(degrees(set_az),  2)

rise_heading = spacestuff.compass_heading(rise_az, 16)
set_heading =  spacestuff.compass_heading(set_az,  16)

print(rise_time)
print(max_time)
print(set_time)
print('Max Alt: {}'.format(max_alt))
print('Az: {} -> {}'.format(rise_az, set_az))
print('Az: {} -> {}'.format(rise_heading, set_heading))
print('Visible: {}'.format(visible))

print('Next visible pass over {}:'.format(loc))

rise_time, rise_az, max_time, max_alt, set_time, set_az, visible = spacestuff.get_next_pass_from_tle(tle, loc, True)

rise_az = round(degrees(rise_az), 2)
max_alt = round(degrees(max_alt), 2)
set_az  = round(degrees(set_az),  2)

rise_heading = spacestuff.compass_heading(rise_az, 16)
set_heading =  spacestuff.compass_heading(set_az,  16)

print(rise_time)
print(max_time)
print(set_time)
print('Max Alt: {}'.format(max_alt))
print('Az: {} -> {}'.format(rise_az, set_az))
print('Az: {} -> {}'.format(rise_heading, set_heading))
print('Visible: {}'.format(visible))

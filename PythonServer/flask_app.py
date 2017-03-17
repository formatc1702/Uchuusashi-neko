
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

from math import degrees
import spacestuff

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'The Flask server is running!'

@app.route('/uchuu/alt_az/<tle0>/<tle1>/<tle2>/<location>')
def alt_az(tle0, tle1, tle2, location):
    alt, az = spacestuff.get_alt_az_from_tle((tle0, tle1, tle2), location)
    alt = round(degrees(alt), 2)
    az  = round(degrees(az),  2)
    response = 'ALT: {}\nAZ:  {}\n'.format(alt, az)
    # response = 'LAT:\t{}\nLON:\t{}\nALT:\t{}\nAZ: \t{}\n\nRISE: {}\tAZ:  {}\nMAX:  {}\tALT: {}\nSET:  {}\tAZ:  {}\n'.format(iss.sublat, iss.sublong, iss.alt, iss.az, rtx, ra, mtx, ma, stx, sa)
    return response

@app.route('/uchuu/next_pass/<tle0>/<tle1>/<tle2>/<location>')
def next_pass(tle0, tle1, tle2, location):
    import datetime
    rise_time, rise_az, max_time, max_alt, set_time, set_az = spacestuff.get_next_pass_from_tle((tle0, tle1, tle2), location)
    # timezone  correction
    # TODO: do it properly
    # to compare to http://www.heavens-above.com/PassSummary.aspx?satid=25544
    rise_time_local = rise_time + datetime.timedelta(0,3600)
    max_time_local  = max_time  + datetime.timedelta(0,3600)
    set_time_local  = set_time  + datetime.timedelta(0,3600)
    rise_az = round(degrees(rise_az), 2)
    max_alt = round(degrees(max_alt), 2)
    set_az  = round(degrees(set_az),  2)
    response = 'RISE: {}\tAZ:  {}\nMAX:  {}\tALT: {}\nSET:  {}\tAZ:  {}\n'.format(rise_time_local, rise_az, max_time_local, max_alt, set_time_local, set_az)
    return response

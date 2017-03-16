
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

from math import degrees
import spacestuff

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask! YEAH'

@app.route('/alt_az/<tle0>/<tle1>/<tle2>/<location>')
def alt_az(tle0, tle1, tle2, location):
    alt, az = spacestuff.get_alt_az_from_tle((tle0, tle1, tle2), location)
    alt = round(degrees(alt), 2)
    az  = round(degrees(az),  2)
    response = 'ALT: {}<br>AZ: {}'.format(alt, az)
    # response = 'LAT:\t{}\nLON:\t{}\nALT:\t{}\nAZ: \t{}\n\nRISE: {}\tAZ:  {}\nMAX:  {}\tALT: {}\nSET:  {}\tAZ:  {}\n'.format(iss.sublat, iss.sublong, iss.alt, iss.az, rtx, ra, mtx, ma, stx, sa)
    return response

@app.route('/next_pass/<tle0>/<tle1>/<tle2>/<location>')
def next_pass(tle0, tle1, tle2, location):
    import datetime
    rise_time, rise_az, max_time, max_alt, set_time, set_az = spacestuff.get_next_pass_from_tle((tle0, tle1, tle2), location)
    # timezone  correction
    # to compare to http://www.heavens-above.com/PassSummary.aspx?satid=25544
    rise_time_local = rise_time + datetime.timedelta(0,3600)
    max_time_local  = max_time  + datetime.timedelta(0,3600)
    set_time_local  = set_time  + datetime.timedelta(0,3600)
    rise_az = round(degrees(rise_az), 2)
    max_alt = round(degrees(max_alt), 2)
    set_az  = round(degrees(set_az),  2)
    response = 'RISE: {}\tAZ:  {}\nMAX:  {}\tALT: {}\nSET:  {}\tAZ:  {}\n'.format(rise_time_local, rise_az, max_time_local, max_alt, set_time_local, set_az)
    return response


@app.route('/alt_az_pred/<line0>/<line1>/<line2>/<location>')
def alt_az_pred(line0,line1,line2,location):
    import ephem
    import datetime
    from math import pi
    loc = ephem.city(location)
    iss = ephem.readtle(line0,line1,line2)
    response = ''
    for i in range(0,60):
        loc.date = datetime.datetime.utcnow() + datetime.timedelta(0, i * 60)
        iss.compute(loc)
        response = response + 'LAT:\t{}\tLON:\t{}\tALT:\t{}\tAZ: \t{}\n'.format(iss.sublat,iss.sublong,iss.alt,iss.az)
    return response

@app.route('/fake.htm')
def fake():
    return '<b>FAT</b> FAIL.'

@app.route('/user/<username>/<number>')
def show_user_profile(username,number):
    # show the user profile for that user
    return 'User {} counts like this: {}'.format(username,number)

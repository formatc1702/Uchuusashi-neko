
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask! YEAH'

@app.route('/alt_az/<line0>/<line1>/<line2>/<location>')
def alt_az(line0,line1,line2,location):
    import ephem
    import datetime
    loc = ephem.city(location)
    loc.date = datetime.datetime.utcnow()
    #line0='ISS (ZARYA)'
    #line1='1 25544U 98067A   17073.59757234  .00003182  00000-0  55149-4 0  9992'
    #line2='2 25544  51.6435 149.8114 0007006 291.5980 211.5204 15.54208770 47040'
    iss = ephem.readtle(line0,line1,line2)
    iss.compute(loc)
    rt, ra, mt, ma, st, sa = loc.next_pass(iss)
    # timezone  correction
    # to compare to http://www.heavens-above.com/PassSummary.aspx?satid=25544
    rtx = rt.datetime() + datetime.timedelta(0,3600)
    mtx = mt.datetime() + datetime.timedelta(0,3600)
    stx = st.datetime() + datetime.timedelta(0,3600)
    response = 'LAT:\t{}\nLON:\t{}\nALT:\t{}\nAZ: \t{}\n\nRISE: {}\tAZ:  {}\nMAX:  {}\tALT: {}\nSET:  {}\tAZ:  {}\n'.format(iss.sublat, iss.sublong, iss.alt, iss.az, rtx, ra, mtx, ma, stx, sa)
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

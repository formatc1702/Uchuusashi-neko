import socket

tle_src    = 'https://www.celestrak.com/NORAD/elements/stations.txt'
alt_az_src = 'http://formatc1702.pythonanywhere.com/uchuu/alt_az/{}/{}/{}/{}'

def http_get(url): # returns socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    return s

def get_tle_from_url(url, obj):
    src = http_get(url)
    while True:
        line = src.readline().decode("utf-8")
        if line:
            if obj in line:
                tle0 = line.strip()
                tle1 = src.readline().decode("utf-8").strip()
                tle2 = src.readline().decode("utf-8").strip()
        else:
            break
    src.close()
    return tle0, tle1, tle2

def get_alt_az_from_tle_and_location(tle, loc):
    url = alt_az_src.format(tle[0],tle[1],tle[2],loc)
    src = http_get(url)
    alt = 'nothing'
    az  = 'nothing'
    while True:
        line = src.readline().decode('utf-8').strip()
        if line:
            if 'ALT:' in line:
                alt = float(line.split(' ')[1])
            if 'AZ:' in line:
                az  = float(line.split(' ')[1])
                break
    src.close()
    return alt, az

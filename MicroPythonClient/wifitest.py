import network
import usocket as socket
import utime as time
import spaceclient


wifi_config = open('wificonfig.txt','r')
my_ap = wifi_config.readline().rstrip()
my_pw = wifi_config.readline().rstrip()
wifi_config.close()
print('Hello!')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print('SSID: ', my_ap)
print('PWD:  ', my_pw)

wlan.connect(my_ap, my_pw)
for i in range(0,40): # attempt to connect
    ip,mask,gateway,dns = wlan.ifconfig()
    if ip == '0.0.0.0': #not connected
        print('.')
        time.sleep(1)
    else: #connected!
        print('Got IP: ', ip)
        tle = spaceclient.get_tle_from_url('https://www.celestrak.com/NORAD/elements/stations.txt','ISS (ZARYA)')
        print(tle)
        spaceclient.get_alt_az_from_tle_and_location(tle, 'Berlin')
        break

import struct

def twos_comp(MSB, LSB):
    comp = MSB * 256 + LSB
    comp = comp - 65536 if comp > 32767 else comp
    return comp

for msb in range(0,256):
    for lsb in range(0,256):
        oldval = struct.unpack("<h",bytes([msb,lsb]))[0]
        newval = twos_comp(msb, lsb)
        if oldval != newval:
            _ = 0 # do nothing
            # print (bin(msb), bin(lsb), '\t', msb, lsb, '\t', bin(newval), newval, oldval)
        else:
            print (bin(msb), bin(lsb), '\t', msb, lsb, '\t', bin(newval), newval, "OK!")

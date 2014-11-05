from base64 import b64decode, b64encode
from urllib import quote, unquote
import requests

BLOCK_SIZE = 16
ALLDATA = b64decode("p4IAaR0MXAqEwrewECBQnWtZcKFwJ+UG3RjIGCotUaV2xb1uW5GDqGys2z0AJoFNpVDvKBqy0UdcRZGW/LdIeHM5cJzrRS0bukZbyy5d2Vg=")
ORIGINAL_IV = bytearray(ALLDATA[:16])


def bust(block,search_range):
    s = requests.Session()

    IV = bytearray(BLOCK_SIZE)
    INTER = bytearray(BLOCK_SIZE)
     
    x = 2
    TRUE_VALUE = bytearray(BLOCK_SIZE)
    for i in reversed(xrange(1,BLOCK_SIZE)):
            OK=False
            print "bf : %d" % i
            for char in search_range:
                    IV[i] = char
                    data = {"vs": b64encode(str(IV+block))}
                    r = s.post("http://nsc2014.synacktiv.com:65480/msg.list", data=data)
                    if "Error" in r.reason:
                            OK=True
                            print "FOUND : 0x%X" % char
                            TRUE_VALUE[i] = char
                            break
            x += 1
            for j in range(BLOCK_SIZE):
                    if 15 - j <= x - 3:
                            INTER[j] = TRUE_VALUE[j]^(17-j)
                            IV[j] = x ^ INTER[j]
            if OK == False:
                print "Bad search_range -> reverse"
                return bust(block,list(reversed(search_range)))
    IV[1]=INTER[1]^0x9C
    IV[2]=INTER[2]^0x0F
    for k in reversed(range(3,16)):
            IV[k] = (0xE) ^ INTER[k]
    print "bf : 0"
    for i in range(0x100):
            IV[0]=i
            data = {"vs": b64encode(str(IV+block))}
            r = s.post("http://nsc2014.synacktiv.com:65480/msg.list", data=data)
            if "incomplete" in r.reason:
                    print "FOUND : 0x%X" % char
                    TRUE_VALUE[0] = i
                    INTER[0] = i ^ 0x78
                    break
    return INTER

if __name__ == '__main__':
        decrypted=""
        for block_num in xrange(0,len(ALLDATA[16:])/16):
                print "bf block : "+str(block_num)
                DATA = bytearray(ALLDATA[block_num*16+16:(block_num+1)*16+16])
                INTER = bust(DATA,range(0x100))
                dec=""
                dec_iv=ALLDATA[block_num*16:(block_num+1)*16]
                for byte in range(BLOCK_SIZE):
                        dec+=chr(INTER[byte]^ord(dec_iv[byte]))
                print "block data "+str(block_num)+" = "+dec.encode("hex")
                decrypted+=dec
        print "Decrypted message : "+decrypted.encode("hex")

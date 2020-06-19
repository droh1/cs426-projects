# File:        lab3_1.py
# Author:      Daniel Roh
# Date:        04/19/19
# Section:     01
# E-mail:      DRoh1@umbc.edu
# Description: A brute force attack program to
#	       decrypt a encrypted message sent by Dr.Gibson

import time
from Crypto.Cipher import DES
from Crypto import Random

def find_key(input, key_length):
    seed = int(input) & 0xffffff
    #seed = int(time.time()) & 0xffffff
    key = bytearray()
    modulus = pow(2, 24)
    a = 1140671485
    b = 12820163

    for i in range(key_length):
       	seed = (a * seed + b) % modulus
       	key.append(seed >> 16) #Changes the seed to hex

    return bytes(key)

#Test if this is the key that we want
#------------------------------------
def check_Key(tKey, cipherTxt):
    #Add check stuff here
    algo = DES.new(tKey, DES.MODE_ECB) #DES = 3DES and DES3 = DES
    msg = algo.decrypt(cipherTxt)

    if msg.find(b"Microsoft") != -1:
        print("Decryped file saved to 'decrypted.doc'")
        f = open("decrypted.doc", "wb")
        f.write(msg)
        f.close()
        return True
    else:
        #print("NOOO") #DEBUG
        return False


#-------------------------------------------------------------
#Main starts here---------------------------------------------
#-------------------------------------------------------------

#note to self, time uses UNIX time which is seconds passed since 1/1/1970
time1 = float(1554825600)
time2 = float(1554847200)
#double check these for est vs gmt conversion

count = time1
cipherTxt = open("encrypted.enc", "rb").read()

while(count <= time2):
    tKey = find_key(count, 8)
    #print(int(count-time1), "SIZE:", len(tKey), " ", tKey) #DEBUG
    check = check_Key(tKey, cipherTxt)
        
    if check == True:
        print("Key Found at time: ",int(count-time1)," Key = ", tKey) #Output
        
    count = count + 1 #Updater

print("DONE") #DEBUG


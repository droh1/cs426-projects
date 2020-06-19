import time

def generate_key(key_length):
    seed = int(time.time()) & 0xffffff
    key = bytearray()
    modulus = pow(2,24)
    a = 1140671485 
    b = 12820163

    for i in range(key_length):
        seed = (a * seed + b) % modulus
        key.append(seed >> 16)

    return bytes(key)

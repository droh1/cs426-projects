# File:        lab3_2.py
# Author:      Daniel Roh
# Date:        04/19/19
# Section:     01
# E-mail:      DRoh1@umbc.edu
# Description: A key generator to find all the possible combination
#              of keys that where used to encrypt a message

import math
import random
import argparse  # library for simple command line argument parsing

##############################################################
# to_int() converts a given plaintext into an integer
# Input:   plaintext; a single string of characters
# Output:  m_int    ; an integer representative of the string
def to_int(plaintext):
    m_int = 0
    for i, char in enumerate(plaintext[::-1]):
        m_int += ord(char) << i * 8

    return m_int

##############################################################
# to_str() converts a given integer back into its plaintext
# Input:   c;     an integer representative of a string
# Output:  c_str; a string of characters
def to_str(c):
    c_str = bytearray()
    while c:
        byte = c & 0xff
        c >>= 8
        c_str.append(byte)
    c_str.reverse()

    return str(bytes(c_str))

#######################################################################
# fermat_primality_test() tests if a number is prime or not,
#         for a specific number of iteration attempts
# Input:  num;      the integer to be tested for primality
#         max_iter; the number of testing attempts to be made
# Output: Boolean;  False if not prime, True if non-primality not seen
def fermat_primality_test(num, max_iter):
    for x in range(1, max_iter):
        a = random.randrange(2, num) #Get a value between [2, num)

        if math.gcd(a, num) > 1: #If the GCD is greater then 1
            return False
       # if (math.pow(a, (num - 1)) % num) != 1: #If the number is not prime
        if pow(a, (num - 1), num) != 1: #If the number is a carmichael number
            return False

    return True
        
###############################################################################
# generate_prime() generates a prime number
# Input:           num_bits; the size of the number to be generated (in bits)
# Output:          num;      a (likely) prime number of the requested bit size
def generate_prime(num_bits):
    test = False
    #start = 10**(num_bits - 1) #Calculate the smallest possible value
    #end = (10**num_bits) - 1 #Calculate the largest possible value
    random.seed() #Get a random seed
    
    while test != True:
        #num = random.randint(start, end)
        num = random.getrandbits(num_bits)
        test = fermat_primality_test(num, 100) #Go test if the value is prime
        
    return num
    
    
###################################################################
# mod_mult_inverse() calculates the modular multiplicative inverse
# Input:  num;     an integer for which we want to find the mod
#                                      multiplicate inverse for
#         modulus; an integer for which we want to find congruence
#                                                  with respect to
# Output: b;       an integer which is the inverse mod modulus
def mod_mult_inverse(num, modulus):
    #print("TODO: ~*~math~*~")
    t_prev, t_curr = 0, 1
    r_prev, r_curr = modulus, num

    while r_curr != 0:
        q = r_prev // r_curr
        (t_prev, t_curr) = (t_curr, t_prev - q * t_curr)
        (r_prev, r_curr) = (r_curr, r_prev - q * r_curr)

    if r_curr > 1:
        return 0
    
    b = t_prev

    if b < 0:
        b = b + modulus #m is modulus
    return b



if __name__ == "__main__":

    # parse command-line arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="modes", dest="mode")

    # key generation mode command-line arguments
    keygen = subparsers.add_parser("keygen")
    keygen.add_argument("-e", type=int, required=True,
                         help="The public exponent e")
    keygen.add_argument("-s", type=int, required=True,
                        choices=[512, 1024, 2048],
                        help="The size of the RSA key in bits")

    # encryption mode command-line arguments
    encrypt = subparsers.add_parser("encrypt")
    encrypt.add_argument("-e", type=int, required=True,
                         help="The public exponent e")
    encrypt.add_argument("-n", type = int, required = True,
                         help = "The public modulus n")
    encrypt.add_argument("--plaintext", required = True,
                         help = "The plaintext")

    # decryption mode command-line arguments
    decrypt = subparsers.add_parser("decrypt")
    decrypt.add_argument("-n", type=int, required=True,
                         help="The public modulus n")
    decrypt.add_argument("-d", type=int, required=True,
                         help="The private exponent d")
    decrypt.add_argument("-c", type=int, required=True, help="The ciphertext")

    args = parser.parse_args()

    # key generation mode
    if args.mode == "keygen":
        # generate p and q
        p = generate_prime(args.s)  # p = None # TODO
        q = generate_prime(args.s)  # q = None # TODO
        print("p:\t{}\nq:\t{}".format(p, q))

        # calculate n
        n = (p * q) # n = None # TODO
        print("n:\t{}".format(n))

        # calculate phi(n)
        phi_n = (p - 1) * (q - 1)  # phi_n = None # TODO
        print("phi_n:\t{}".format(phi_n))

        # calculate the private exponent d
        d = mod_mult_inverse(args.e, phi_n)  # d = None # TODO
        #d = pow(math.e, -1, n)
        print("e:\t{}\nd:\t{}".format(args.e, d))

    # encryption mode
    elif args.mode == "encrypt":
        # generate the integer m from the plaintext
        m = to_int(args.plaintext) #args.plaintext # m = None # TODO
        
        # calculate the ciphertext c
        c = pow(m, args.e, args.n) # c = None # TODO
        print("c:\t{}".format(c))

    # decryption mode
    elif args.mode == "decrypt":
        # calculate the decrypted integer m
        m = pow(args.c, args.d, args.n) #m = None # TODO

        # print out the plaintext from the decrypted integer m
        print("m:\t{}".format(to_str(m)))
        
    else:
        print("Invalid mode. Use python lab3_2.py -h for help.")

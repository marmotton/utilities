#!/usr/bin/python3

import sys


def b64_unhide(str):
    base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    # Extract the hidden bits
    bin_str = ''
    for line in str.split('\n'):
        n_equals = line.count('=')
        n_hidden_bits = 2 * n_equals

        if n_hidden_bits:
            last_b64_value = base64chars.index(line[-n_equals - 1])
            hidden_bits = last_b64_value & (2 ** n_hidden_bits - 1)

            bin_str += "{:0{}b}".format(hidden_bits, n_hidden_bits)

    return bin_str_to_ascii(bin_str)


def b32_unhide(str):
    base32chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'

    # Extract the hidden bits
    bin_str = ''
    for line in str.split('\n'):
        n_equals = line.count('=')
        hidden_bits_lookup = {0: 0,  # n_equals : n_hidden_bits
                              1: 3,
                              3: 1,
                              4: 4,
                              6: 2}
        n_hidden_bits = hidden_bits_lookup[n_equals]

        if n_hidden_bits:
            last_b32_value = base32chars.index(line[-n_equals - 1])
            hidden_bits = last_b32_value & (2 ** n_hidden_bits - 1)

            bin_str += "{:0{}b}".format(hidden_bits, n_hidden_bits)

    return bin_str_to_ascii(bin_str)


def bin_str_to_ascii(bin_str):
    # Split the bits into bytes and convert them into an ascii string
    out_str = ''
    for i in range(0, len(bin_str), 8):
        byte_str = bin_str[i:i + 8]  # the byte as a string of '0' and '1'
        number = int(byte_str, 2)  # the byte

        out_str += chr(number)

    return out_str


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        print(
'''Usage: unhide_b64.py ENCODING

This program reads base64 or base32 text from STDIN and
writes the data that is hidden in the padding bits to STDOUT
as ASCII text.

Possible values for ENCODING:
    -b64 : Base64 input
    -b32 : Base32 input

Example usage:
cat encoded.txt | ./unhide_b64.py -b64 > out.txt''')
        sys.exit()

    if sys.argv[1] == '-b32':
        print(b32_unhide(sys.stdin.read()))
    elif sys.argv[1] == '-b64':
        print(b64_unhide(sys.stdin.read()))

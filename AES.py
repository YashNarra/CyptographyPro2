# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
AES encryption system, 128 bit key, 10 rounds.
"""
from CommonMethod import *


class AES(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.round = 0
        return cls.__instance

    def __init__(self, original_key, plain_text):
        self.original_key = group_input_text(original_key)
        self.plain_text = group_input_text(plain_text)
        self.keys = []
        self.output = []

    def __str__(self):
        return "AES 128 bit key, 10 rounds encryption system."

    def encryption(self):
        key = self.KS(key=self.original_key, i=self.round)
        ark_msg = self.ARK(key=key, msg=self.plain_text)
        self.keys.append([key])
        self.output.append([ark_msg])
        self.round += 1
        while self.round <= 10:
            if self.round != 10:
                key = self.KS(key, i=self.round)
                ark_msg = self.ARK(key=key, msg=self.MC(msg=self.SR(msg=self.BS(msg=ark_msg))))
            else:
                ark_msg = self.ARK(key=key, msg=self.SR(msg=self.BS(msg=ark_msg)))
            self.keys.append([key])
            self.output.append([ark_msg])
            self.round += 1

        return ark_msg

    # Add RoundKey
    def ARK(self, key, msg):
        n = len(msg)
        for i in range(n):
            for j in range(n):
                msg[i][j] = bit_xor_operation(msg[i][j], key[i][j], batch=False)
                # msg[i][j] %= 8
        return msg

    # TEST PASS
    # ByteSub transformation
    def BS(self, msg, matrix=True):
        s_box = [
            [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
            [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
            [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
        ]
        if matrix:
            m, n = len(msg), len(msg[0])
            new_msg = [[None for _ in range(m)] for _ in range(n)]
            for i in range(m):
                for j in range(n):
                    len_index = len(msg[i][j]) // 2
                    if len_index < 1:
                        x, y = 0, msg[i][j]
                    else:
                        x, y = int(str(msg[i][j])[:len_index], 16), int(str(msg[i][j])[len_index:], 16)
                    new_msg[i][j] = s_box[x][y]
        else:
            n = len(msg)
            new_msg = [None] * n
            for i in range(n):
                len_index = len(str(msg[i])) // 2
                if len_index < 1:
                    x, y = 0, msg[i]
                else:
                    x, y = int(str(msg[i])[:len_index], 16), int(str(msg[i])[len_index:], 16)
                new_msg[i] = s_box[x][y]
        return new_msg

    # TEST PASS
    # ShiftRow Transformation
    def SR(self, msg):
        m, n = len(msg), len(msg[0])
        new_msg = [[None for _ in range(m)] for _ in range(n)]
        shift = 0
        for i in range(m):
            new_msg[i] = msg[i][shift:] + msg[i][:shift]
            shift += 1
        return new_msg

    # MixColumn
    def MC(self, msg):
        M = [[2, 3, 1, 1],
             [1, 2, 3, 1],
             [1, 1, 2, 3],
             [3, 1, 1, 2]]
        n = len(msg)
        new_msg = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    value = poly_mul(bin_to_poly_coefficient(bin(M[i][k]))[::-1],
                                     bin_to_poly_coefficient(bin(msg[k][j]))[::-1])
                    _, value = poly_div(a=coefficient_to_int(value))
                    new_msg[i][j] += value
        return new_msg

    # OUTPUT INCORRECT
    # Key Schedule
    def KS(self, key, i):
        print(f"key: {key}, i: {i}")
        m, n = len(key), len(key[0])
        # Round 0 Key
        if i == 0:
            w = [[None for _ in range(n)] for _ in range(m)]
            for j in range(m):
                for k in range(n):
                    w[j][k] = key[k][j]
            w0, w1, w2, w3 = w[0], w[1], w[2], w[3]
            print(f"Round 0 key: {[w0, w1, w2, w3]}\n")
            return [w0, w1, w2, w3]

        w0, w1, w2, w3 = key
        print(f"w0: {w0}, w1: {w1}, w2: {w2}, w3: {w3}")
        w3 = [x % 8 for x in w3]
        w3 = w3[1:] + [w3[0]]
        print(f"new_w3: {w3}")
        w3 = self.BS(w3[1:] + [w3[0]], matrix=False)
        print(f"Tw3: {w3}")
        w3[0] = bit_xor_operation(w3[0], pow(2, i - 1) % 8, batch=False)
        print(f"Tw3: {w3}")
        new_w0 = bit_xor_operation(w0, w3)
        print(f"new_w0: {new_w0}")
        new_w1 = bit_xor_operation(w1, new_w0)
        print(f"new_w1: {new_w1}")
        new_w2 = bit_xor_operation(w2, new_w1)
        print(f"new_w2: {new_w2}")
        new_w3 = bit_xor_operation(w3, new_w2)
        print(f"new_w3: {new_w3}")
        return [new_w0, new_w1, new_w2, new_w3]


if __name__ == "__main__":
    # plain_text = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff"
    # original_key = "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f"
    plain_text = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
    original_key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    print(f"plain_text: {plain_text}\noriginal_key: {original_key}\n")
    obj = AES(original_key, plain_text)
    # print(obj.KS(key=group_input_text(original_key), i=1))
    ark_msg = obj.ARK(key=obj.KS(key=group_input_text(original_key), i=0), msg=group_input_text(plain_text))
    print(f"ark_msg: {ark_msg}")
    s1 = []
    for a, b, c, d in ark_msg:
        s1 += [a, b, c, d]
    s1 = [hex(x) for x in s1]
    print(f"s1: {s1}")
    # decimal_ark, hex_ark = [], []
    # for i in range(4):
    #     for j in range(4):
    #         decimal_ark.append(ark_msg[i][j] % 8)
    #         hex_ark.append(hex(ark_msg[i][j]))
    #         # print("decimal" + str(ark_msg[i][j] % 8))
    #         # print("hex" + str(hex(ark_msg[i][j] % 8)))
    # print(f"decimal_ark: {decimal_ark}\nhex_ark: {hex_ark}\n")

    # print(obj.SR(msg=group_input_text(plain_text)))
    # print(obj.BS())


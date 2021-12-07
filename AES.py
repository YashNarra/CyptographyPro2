# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
AES encryption system, 128 bit key, 10 rounds.
"""
from CommonMethod import *
from data import AESData


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
        self.mod = pow(2, 8)

    def __str__(self):
        return "AES 128 bit key, 10 rounds encryption system."

    def encryption(self, modified=False):
        key = self.original_key
        ark_msg = self.ARK(key=key, msg=self.plain_text)
        self.keys.append([key])
        self.output.append([ark_msg])
        self.round += 1
        while self.round <= 10:
            if self.round != 10:
                key = self.KS(key, i=self.round)
                ark_msg = self.ARK(key=key, msg=self.MC(msg=self.SR(msg=self.BS(msg=ark_msg, modified=modified))))
            else:
                ark_msg = self.ARK(key=key, msg=self.SR(msg=self.BS(msg=ark_msg, modified=modified)))
            self.keys.append([key])
            self.output.append([ark_msg])
            self.round += 1

        return ark_msg

    # TEST PASS
    # Add RoundKey
    def ARK(self, key, msg):
        n = len(msg)
        for i in range(n):
            for j in range(n):
                msg[i][j] = bit_xor_operation(msg[i][j], key[i][j], batch=False)
        return msg

    # TEST PASS
    # ByteSub transformation
    def BS(self, msg, matrix=True, modified=False):
        if modified:
            s_box = AESData.modified_s_box
        else:
            s_box = AESData.s_box
        if matrix:
            m, n = len(msg), len(msg[0])
            new_msg = [[None for _ in range(m)] for _ in range(n)]
            for i in range(m):
                for j in range(n):
                    msg[i][j] = hex(msg[i][j])[2:]
                    len_index = len(str(msg[i][j])) // 2
                    if len_index < 1:
                        x, y = 0, int(msg[i][j], 16)
                    else:
                        x, y = int(str(msg[i][j])[:len_index], 16), int(str(msg[i][j])[len_index:], 16)
                    # print(f"x, y: {x}, {y}")
                    new_msg[i][j] = s_box[x][y]
        else:
            n = len(msg)
            new_msg = [None] * n
            for i in range(n):
                msg[i] = hex(msg[i])[2:]
                # print(f"msg[i]: {msg[i]}")
                len_index = len(str(msg[i])) // 2
                if len_index < 1:
                    x, y = 0, int(msg[i], 16)
                else:
                    x, y = int(str(msg[i])[:len_index], 16), int(str(msg[i])[len_index:], 16)
                # print(f"hex x, y: {x}, {y}")
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
        M = AESData.M
        n = len(msg)
        new_msg = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    value = poly_mul(bin_to_poly_coefficient(bin(M[i][k]))[::-1],
                                     bin_to_poly_coefficient(bin(msg[k][j]))[::-1])
                    _, value = poly_div(a=coefficient_to_int(value))
                    print(f"value: {value}, bin value: {bin(value)}, hex value: {hex(value)}")
                    new_msg[i][j] += value
                new_msg[i][j] %= self.mod
        return new_msg

    # TEST PASS
    # Key Schedule
    def KS(self, key, i):
        w0, w1, w2, w3 = key
        original_w3 = w3
        w3 = [x % self.mod for x in w3]
        w3 = w3[1:] + [w3[0]]
        w3 = self.BS(w3, matrix=False)
        r = pow(2, i - 1) % 8
        w3[0] = bit_xor_operation(w3[0], r, batch=False)
        new_w0 = bit_xor_operation(w0, w3)
        new_w1 = bit_xor_operation(w1, new_w0)
        new_w2 = bit_xor_operation(w2, new_w1)
        new_w3 = bit_xor_operation(original_w3, new_w2)
        return [new_w0, new_w1, new_w2, new_w3]


if __name__ == "__main__":
    plain_text = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
    original_key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
    # print(f"plain_text: {group_input_text(plain_text)}\noriginal_key: {original_key}\n")
    obj = AES(original_key, plain_text)

    # ROUND 0
    key = group_input_text(original_key)
    print(f"ROUND 0 key: {get_other_format_msg(key)}")
    ark_msg = group_input_text(plain_text)
    ark_msg = obj.ARK(key=key, msg=ark_msg)
    print(f"ROUND 0 ark_msg: {get_other_format_msg(ark_msg)}")
    print("*****************\n")

    # ROUND 1
    key = obj.KS(key=key, i=1)
    print(f"ROUND 1 key: {get_other_format_msg(key)}")
    bs_msg = obj.BS(msg=ark_msg)
    print(f"ROUND 1 bs_msg: {get_other_format_msg(bs_msg)}")
    sr_msg = obj.SR(msg=bs_msg)
    print(f"ROUND 1 sr_msg: {get_other_format_msg(sr_msg)}")

    print(f"ROUND 1 sr_msg(int) C: {group_input_text(get_other_format_msg(sr_msg, _format='int'))}")
    print(f"ROUND 1 sr_msg(bin) C: {group_input_text(get_other_format_msg(sr_msg, _format='bin'))}")
    print(f"M matrix for MC(bin): {get_other_format_msg(AESData.M, _format='bin')}")
    mc_msg = obj.MC(msg=sr_msg)
    print(f"ROUND 1 mc_msg: {get_other_format_msg(mc_msg)}\n")

    ark_msg = obj.ARK(key=key, msg=mc_msg)
    print(f"ROUND 1 ark_msg: {get_other_format_msg(ark_msg)}")





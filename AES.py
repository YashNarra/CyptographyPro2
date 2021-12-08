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

    def encryption(self, modified=True):
        print("----------------------------------------------------------")
        print(f"ID1 = {AESData.students[0][1]} ({AESData.students[0][0]})")
        print(f"ID2 = {AESData.students[1][1]} ({AESData.students[1][0]})")
        print(f"ID3 = {AESData.students[2][1]} ({AESData.students[2][0]})")
        print(f"Group Code (A, B) = {AESData.group_code}")
        print(f"Assigned Plaintext and Key:\n   {get_other_format_msg(AESData.plain_text)}\n"
              f"   {get_other_format_msg(AESData.original_key)}\n")
        print(f"The program is written in Python 3.8 for operating system MacOS (Unix).")
        print("----------------------------------------------------------")
        print("Key Schedule Results for Each Round with the modified AES:")
        print("----------------------------------------------------------")
        self.__encryption(modified=modified)
        for i, key in enumerate(self.keys):
            print(f"Round {i}:\n   Key: {get_other_format_msg(key)}")
        print("----------------------------------------------------------")
        for i, output in enumerate(self.output):
            if i == 0:
                print(f"Round {i}:\n-----Start: {get_other_format_msg(AESData.plain_text)}\n"
                      f"----Output: {str_to_hex(output)}")
            elif i == 10:
                print(f"Round {i}:\n----Output: {output}")
            else:
                print(f"Round {i}:\n----Output: {str_to_hex(output)}")
        print("----------------------------------------------------------")

    def __encryption(self, modified):
        key = self.original_key
        ark_msg = self.ARK(key=key, msg=self.plain_text, m=False)
        self.keys.append(key)
        self.output.append(ark_msg)
        self.round += 1
        while self.round <= 10:
            if self.round != 10:
                key = self.KS(key, i=self.round)
                ark_msg = self.ARK(key=key, msg=self.MC(msg=self.SR(msg=self.BS(msg=ark_msg, modified=modified))))
            else:
                key = self.KS(key, i=self.round)
                ark_msg = self.ARK(key=key, msg=self.SR(msg=self.BS(msg=ark_msg, modified=modified)))
                ark_msg = get_other_format_msg(ark_msg)
            self.keys.append(key)
            self.output.append(ark_msg)
            self.round += 1

        return ark_msg

    # Add RoundKey
    def ARK(self, key, msg, m=True):
        n = len(msg)
        new_msg = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if m:
                    mapping = AESData.mapping
                    x, y = mapping[i][j]
                else:
                    x, y = i, j
                msg[x][y] = bit_xor_operation(msg[x][y], key[i][j], batch=False)
        if m:
            new_msg = [[None for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    mapping = AESData.mapping
                    ii, jj = mapping[i][j]
                    new_msg[i][j] = msg[ii][jj]
        return new_msg if m else msg

    # ByteSub transformation
    def BS(self, msg, matrix=True, modified=True):
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
                    new_msg[i][j] = s_box[x][y]
        else:
            n = len(msg)
            new_msg = [None] * n
            for i in range(n):
                msg[i] = hex(msg[i])[2:]
                len_index = len(str(msg[i])) // 2
                if len_index < 1:
                    x, y = 0, int(msg[i], 16)
                else:
                    x, y = int(str(msg[i])[:len_index], 16), int(str(msg[i])[len_index:], 16)
                new_msg[i] = s_box[x][y]
        return new_msg

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
                new_msg[i][j] = galois_mul(M[i][0], msg[0][j]) ^ galois_mul(M[i][1], msg[1][j]) ^ \
                                galois_mul(M[i][2], msg[2][j]) ^ galois_mul(M[i][3], msg[3][j])
        return new_msg

    # Key Schedule
    def KS(self, key, i, modified=True):
        w0, w1, w2, w3 = key
        original_w3 = w3
        w3 = [x % self.mod for x in w3]
        w3 = w3[1:] + [w3[0]]
        w3 = self.BS(w3, matrix=False, modified=modified)
        if i < 9:
            r = pow(2, i - 1) % self.mod
        elif i == 9:
            r = 27
        elif i == 10:
            r = 54
        w3[0] = bit_xor_operation(w3[0], r, batch=False)
        new_w0 = bit_xor_operation(w0, w3)
        new_w1 = bit_xor_operation(w1, new_w0)
        new_w2 = bit_xor_operation(w2, new_w1)
        new_w3 = bit_xor_operation(original_w3, new_w2)
        return [new_w0, new_w1, new_w2, new_w3]


if __name__ == "__main__":
    obj = AES(original_key=AESData.original_key, plain_text=AESData.plain_text)
    # obj.encryption(modified=False)
    obj.encryption(modified=True)

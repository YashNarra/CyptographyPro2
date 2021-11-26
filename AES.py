# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
AES encryption system, 128 bit key, 10 rounds.
"""


class AES(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.round = 0
        return cls.__instance

    def __init__(self, original_key, plain_text):
        self.original_key = original_key
        self.plain_text = plain_text

    def __str__(self):
        pass

    def encryption(self):
        key = self.KS(key=self.original_key)
        ark_msg = self.ARK(key=self.original_key, msg=self.plain_text)
        self.round += 1
        while self.round <= 10:
            if self.round != 10:
                ark_msg = self.ARK(key=key, msg=self.MC(msg=self.SR(msg=self.BS(msg=ark_msg))))
                key = self.KS(key)
            else:
                ark_msg = self.ARK(key=key, msg=self.SR(msg=self.BS(msg=ark_msg)))
            self.round += 1

        return ark_msg

    # Add RoundKey
    def ARK(self, key, msg):
        return msg

    # ByteSub transformation
    def BS(self, msg):
        pass

    # ShiftRow Transformation
    def SR(self, msg):
        pass

    # MixColumn
    def MC(self, msg):
        pass

    def KS(self, key):
        pass
        return key


if __name__ == "__main__":
    original_key = ""
    plain_text = ""
    obj = AES(original_key, plain_text)
    print(obj.BS())

# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
Common method collection.
"""


def group_input_text(text, size=4):
    """
    Convert 128 bits input to 16 bytes of 8 bits.
    :param text: [str] input text.
    :param size: [int] default value is 4.
    :return: [2-D list] converted text.
    """
    if isinstance(text, str):
        text = text.split()
    return [text[i:i+size] for i in range(0, len(text), size)]


def bit_xor_operation(a, b, batch=True):
    """
    Bit wise xor operation between two decimal/hexadecimal.
    :param a: [int]
    :param b: [int]
    :param batch: [boolean] convert only a number or a list of numbers, default value is True.
    :return: [int] binary result.
    """
    if batch:
        return [a[i] ^ b[i] for i in range(len(a))]
    else:
        return a ^ b


def get_other_format_msg(msg, _format="hex"):
    """
    Get the hexadecimal or binary format message list.
    :param msg: [list] decimal format message list.
    :param _format: [str] "hex" or "bin", default is "hex".
    :return: [list] hexadecimal or binary format message list.
    """
    new_msg = []
    if isinstance(msg[0], list):
        for a, b, c, d in msg:
            if isinstance(a, list):
                new_msg = a + b + c + d
            else:
                new_msg += [a, b, c, d]
    msg = new_msg if new_msg else msg
    new_msg = [int(x) for x in msg]
    if _format == "hex":
        new_msg = [hex(x) for x in msg]
    elif _format == "bin":
        new_msg = [bin(x) for x in msg]
    return new_msg


def str_to_hex(msg):
    new_msg = []
    for i in range(4):
        for j in range(4):
            new_msg.append(hex(int(msg[i][j], 16)))
    return new_msg


def galois_mul(a, b):
    """
    Galois multiplication of 8 bit characters.
    :param a: [int]
    :param b: [int]
    :return: result.
    """
    p = 0
    for counter in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        a &= 0xFF
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
    return p

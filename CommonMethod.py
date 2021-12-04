# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
Common method collection.
"""


def decimal_conversion(decimal, binary=False, batch=True):
    """
    Convert decimal to binary or hexadecimal.
    :param decimal: [str] or [list] decimal to be converted.
    :param binary: [boolean] if convert to binary it is True otherwise if False, default value is False.
    :param batch: [boolean] convert only a number or a list of numbers, default value is True.
    :return: [str] or [list] converted number.
    """
    if batch:
        if binary:
            return [bin(d) for d in decimal]
        else:
            return [hex(d) for d in decimal]
    else:
        return bin(decimal) if binary else hex(decimal)


def str_conversion(decimal, binary=False, batch=True):
    """
    Convert str to binary or hexadecimal.
    :param decimal: [str] or [list] decimal to be converted.
    :param binary: [boolean] if convert to binary it is True otherwise if False, default value is False.
    :param batch: [boolean] convert only a number or a list of numbers, default value is True.
    :return: [str] or [list] converted str.
    """
    prefix = "0b" if binary else "0x"
    if batch:
        return [hex(prefix + d) for d in decimal]
    else:
        return prefix + decimal


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


def bin_to_poly(bin_item, poly_degree=8):
    """
    Convert binary number to polynomial coefficient.
    :param bin_item: [str] binary number.
    :param poly_degree: degree of the polynomial function, default is 8.
    :return: [list] coefficient list.
    """
    bin_item = bin_item.split("b")[-1]
    bin_item = "0" * (poly_degree - len(bin_item)) + bin_item
    return [i for i in range(poly_degree) if bin_item[::-1][i] == "1"]


def bit_xor_operation(a, b, batch=True):
    """
    Bit wise xor operation between two decimal/hexadecimal.
    :param a: [int]
    :param b: [int]
    :param batch: [boolean] convert only a number or a list of numbers, default value is True.
    :return: [int] binary result.
    """
    if batch:
        return [bin(a[i] ^ b[i]).count("1") for i in range(len(a))]
        # return [bin(a[i]).split("b")[-1] ^ bin(b[i]).split("b")[-1] for i in range(len(a))]
    else:
        return bin(a ^ b).count("1")
        # return bin(a).split("b")[-1] ^ bin(b).split("b")[-1]


if __name__ == "__main__":
    text = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff"
    print(group_input_text(text))

    # bin_item = "00000011"
    # bin_item = '0b1100011'
    # print(bin_to_poly(bin_item))
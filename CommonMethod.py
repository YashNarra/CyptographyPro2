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


if __name__ == "__main__":
    # text = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff"
    # print(group_input_text(text))

    # bin_item = "00000011"
    bin_item = '0b1100011'
    print(bin_to_poly(bin_item))
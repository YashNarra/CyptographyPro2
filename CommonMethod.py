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


if __name__ == "__main__":
    text = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff"
    print(group_input_text(text))

# -*- coding: utf-8 -*-
"""
@date: 2021/11/25

@author: Renting Tong

@description:
Common method collection.
"""
from numpy.polynomial import polynomial as p


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


def bin_to_poly_exponent(bin_item, poly_degree=8):
    """
    Convert binary number to polynomial exponent.
    :param bin_item: [str] binary number.
    :param poly_degree: [int] degree of the polynomial function, default is 8.
    :return: [list] exponent list.
    """
    bin_item = bin_item.split("b")[-1]
    bin_item = "0" * (poly_degree - len(bin_item)) + bin_item
    return [i for i in range(poly_degree) if bin_item[::-1][i] == "1"]


def bin_to_poly_coefficient(bin_item, poly_degree=8):
    """
    Convert binary number to polynomial coefficient.
    :param bin_item: [str] binary number.
    :param poly_degree: [int] degree of the polynomial function, default is 8.
    :return: [list] sequences of coefficients, from highest order term to lowest.
    """
    bin_item = bin_item.split("b")[-1]
    bin_item = "0" * (poly_degree - len(bin_item)) + bin_item
    return [int(x) for x in bin_item]


def bit_xor_operation(a, b, batch=True):
    """
    Bit wise xor operation between two decimal/hexadecimal.
    :param a: [int]
    :param b: [int]
    :param batch: [boolean] convert only a number or a list of numbers, default value is True.
    :return: [int] binary result.
    """
    if batch:
        # return [bin(a[i]).split("b")[-1] ^ bin(b[i]).split("b")[-1] for i in range(len(a))]
        # return [bin(a[i] ^ b[i]).count("1") for i in range(len(a))]
        return [a[i] ^ b[i] for i in range(len(a))]
    else:
        # return bin(a).split("b")[-1] ^ bin(b).split("b")[-1]
        # return bin(a ^ b).count("1")
        return a ^ b


def poly_mul(a, b):
    """
    Calculation polynomial multiplication.
    :param a: [list] sequences of coefficients, from lowest order term to highest.
    :param b: [list] sequences of coefficients, from lowest order term to highest
    :return: [list] sequences of coefficients, from highest order term to lowest.
    """
    if not isinstance(a, list):
        a = [int(x) for x in a if x != " "][::-1]
    if not isinstance(b, list):
        b = [int(x) for x in b if x != " "][::-1]
    r = list(map(int, p.polymul(a, b)[::-1]))
    r = [x % 2 for x in r]
    return r


def poly_div(a, b=283):
    """
    Calculation polynomial division.
    :param a: [int] decimal representation of polynomial coefficient sequences.
    :param b: [int] decimal representation of polynomial coefficient sequences, default value is 283,
    in GF(2^8), f(x) = x^8 + x^4 + x^3 + x + 1.
    :return: [int] the quotient q and remainder r.
    """
    m, n = nonzero_msb(a), nonzero_msb(b)
    if m < n:
        return [0, a]
    a = a ^ (b << (m - n))
    [q, r] = poly_div(a, b)
    return [(1 << (m - n)) | q, r]


def coefficient_to_int(co):
    """
    Transfer polynomial coefficient sequences to decimal.
    :param co: [list] polynomial coefficient sequences, from highest order term to lowest.
    :return: [int] decimal representation.
    """
    res = 0
    n = len(co)
    for i in range(n):
        if co[i]:
            res += pow(2, n - i - 1)
    return res


def nonzero_msb(value):
    """
    Get highest exponent.
    """
    value = "{:09b}".format(value)
    for i in range(9):
        if int(value[i]):
            return 9 - i


def get_other_format_msg(msg, _format="hex"):
    """
    Get the hexadecimal or binary format message list.
    :param msg: [list] decimal format message list.
    :param _format: [str] "hex" or "bin", default is "hex".
    :return: [list] hexadecimal or binary format message list.
    """
    new_msg = []
    for a, b, c, d in msg:
        new_msg += [a, b, c, d]
    if _format == "hex":
        new_msg = [hex(x) for x in new_msg]
    elif _format == "bin":
        new_msg = [bin(x) for x in new_msg]
    else:
        new_msg = [int(x) for x in new_msg]
    return new_msg


if __name__ == "__main__":
    # text = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff"
    # print(group_input_text(text))

    bin_item = "00000011"
    # bin_item = '0b1100011'
    print(bin_to_poly_exponent(bin_item))
    print(bin_to_poly_coefficient(bin_item))

    a = "00000011"
    b = "10101100"
    r = poly_mul(a, b)
    print(f"poly mul: {r}\n")
    print(f"coefficient_to_int: {coefficient_to_int(r)}")
    q, r = poly_div(a=coefficient_to_int(r))
    print(f"after mod f(x), q: {q}, r: {r}, bin(r): {bin(r)}")


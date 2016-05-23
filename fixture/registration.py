# -*- coding: utf-8 -*-

import random
import string
import encodings


class RegistrationHelper:

    def get_phone_number(self, len):
        symbols = string.digits
        preliminary = "".join([random.choice(symbols) for i in range(len - 1)])
        return "9" + preliminary

    def get_first_and_last_name(self, len):
        lowercase_symbols = string.ascii_lowercase
        uppercase_symbol = string.ascii_uppercase
        first_letter = random.choice(uppercase_symbol)
        following_letters = "".join([random.choice(lowercase_symbols) for i in range(len)])
        return first_letter + following_letters

    def get_phoneNumber_for_comparison(self, phone_number):
        b = phone_number[3:6]
        c = phone_number[6:8]
        d = phone_number[-2:]
        return b + "-" + c + "-" + d

    def get_prefix_phone_number(self, phone_number):
        return phone_number[0:3]




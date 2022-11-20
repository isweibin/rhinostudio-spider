# SPDX-FileCopyrightText: 2022 Weibin Jia <me@isweibin.com>
# SPDX-License-Identifier: Apache-2.0

import string


def merge_key_elements(key, a, b=1):
    """Merge two elements of the key into one. a and b are their index."""
    merged_element = chr(ord(key[a]) - 97 + 26*(int(key[a+1]) + b) - 97)
    return merged_element


def get_decrypted_key(key, a, b, c, d):
    """Merge key elements, combine elements to get full decrypted key."""
    A = merge_key_elements(key, a)
    B = merge_key_elements(key, b)
    C = merge_key_elements(key, c)
    D = merge_key_elements(key, d, 2)

    decrypted_key = key[:a] + A + key[a+2:b] + B + key[b+2:c] + C + key[c+2:d] + D + key[d+2:]
    return decrypted_key


def decrypt_key(key, ver=3):
    """Decrypt key for different versions of qiqiuyun video."""
    decrypted_key = []
    key_length = len(key)

    if key_length == 17:
        decrypted_key = [key[int(_)] for _ in '8 9 2 3 4 5 6 7 0 1 10 11 12 13 14 15'.split()]
    elif key_length == 20:
        _ = string.digits + string.ascii_lowercase
        u = _.index(key[0]) % 2
        u = _.index(key[u + 1]) % 3

        if ver == 3:
            if u == 0:
                decrypted_key = [key[int(_)] for _ in '0 1 2 3 4 15 16 17 18 10 11 12 13 6 7 8'.split()]
            elif u == 1:
                decrypted_key = [key[int(_)] for _ in '0 1 2 8 9 10 11 12 18 17 16 15 14 4 5 6'.split()]
            elif u == 2:
                decrypted_key = get_decrypted_key(key, 5, 9, 13, 17)
        elif ver == 2:
            if u == 0:
                decrypted_key = [key[int(_)] for _ in '0 1 2 12 13 14 15 16 17 18 4 5 6 7 9 10'.split()]
            elif u == 1:
                decrypted_key = [key[int(_)] for _ in '0 1 2 3 4 12 13 14 7 6 18 17 15 8 9 10'.split()]
            elif u == 2:
                decrypted_key = get_decrypted_key(key, 3, 8, 14, 18)
        else:
            if u == 0:
                decrypted_key = [key[int(_)] for _ in '0 1 2 3 4 5 6 7 8 10 11 12 14 15 16 18'.split()]
            elif u == 1:
                decrypted_key = [key[int(_)] for _ in '0 1 2 3 4 5 6 7 18 16 15 13 12 11 10 8'.split()]
            elif u == 2:
                decrypted_key = get_decrypted_key(key, 8, 10, 15, 17)

    return ''.join(decrypted_key).encode('utf8')

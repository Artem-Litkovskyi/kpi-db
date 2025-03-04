import os


PATH_ALPHA = ('alphabets', 'codes')
FILES_ALPHA = ('uk.txt', 'en.txt')
STRING_LENGTH = 4
PLACES_PER_CHAR = 2

alphas = []


def load_alpha():
    global alphas
    alphas = tuple(_read_alpha(x) for x in FILES_ALPHA)

def alpha_hash(string: str):
    hash_value = 0

    alpha_index = _get_alpha_index(string)

    i = 1
    for c in string:
        char_code = _get_char_code(c.upper(), alpha_index)
        if char_code < 0:
            continue
        hash_value += char_code * 10 ** (PLACES_PER_CHAR * (STRING_LENGTH - i))
        i += 1
        if i > STRING_LENGTH:
            break

    hash_value += (alpha_index + 1) * 10 ** (PLACES_PER_CHAR * STRING_LENGTH)

    return hash_value

def _get_alpha_index(string: str):
    for c in string:
        for i, a in enumerate(alphas):
            if c.upper() in a:
                return i
    raise ValueError(
        'can\'t get a hash for the string \'%s\', because it doesn\'t contain any supported character' % string)

def _get_char_code(char: str, alpha_index: int):
    if char not in alphas[alpha_index]:
        return -1

    return alphas[alpha_index].index(char)

def _read_alpha(filename):
    with open(os.path.join(*PATH_ALPHA, filename), 'r') as f:
        return f.read()

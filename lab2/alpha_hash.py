import os


PATH_ALPHA = ('alphabets', 'codes')
FILES_ALPHA = ('uk.txt', 'en.txt')
STRING_LENGTH = 10

alphas = []


def load_alpha():
    global alphas
    alphas = tuple(_read_alpha(x) for x in FILES_ALPHA)

def alpha_hash(string: str):
    hash_value = 0

    short_string = string[:STRING_LENGTH]

    alpha_index = _get_alpha_index(short_string)

    i = 1
    for c in short_string:
        char_code = _get_char_code(c.upper(), alpha_index)
        if char_code < 0:
            continue
        hash_value += char_code * 10 ** (STRING_LENGTH - i)
        i += 1

    hash_value += (alpha_index + 1) * 10 ** STRING_LENGTH

    return hash_value

def _get_alpha_index(string: str):
    for c in string:
        for i, a in enumerate(alphas):
            if c.upper() in a:
                return i
    raise ValueError(
        'can\'t get a hash for the string \'%s\', because it doesn\'t contain any supported character' % string)

def _get_char_code(char: str, alpha_index: int):
    char_code = 0

    for c in alphas[alpha_index]:
        if c == '\n':
            char_code += 1
        elif c == char:
            return char_code

    return -1

def _read_alpha(filename):
    with open(os.path.join(*PATH_ALPHA, filename), 'r') as f:
        return f.read()

STRING_LENGTH = 4
PLACES_PER_CHAR = 2

ALPHAS = (
    'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ',  # Uk
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # En
)


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
        for i, a in enumerate(ALPHAS):
            if c.upper() in a:
                return i
    raise ValueError(
        'can\'t get a hash for the string \'%s\', because it doesn\'t contain any supported character' % string)


def _get_char_code(char: str, alpha_index: int):
    if char not in ALPHAS[alpha_index]:
        return -1

    return ALPHAS[alpha_index].index(char)

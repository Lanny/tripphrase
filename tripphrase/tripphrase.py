#!/usr/bin/env python
import hashlib
import os.path

WORD_TYPES = ('noun', 'verb', 'adj', 'adv', 'article')

TEMPLATES = (
    ('verb', 'article', 'adj', 'noun'),
    ('article', 'adj', 'adj', 'noun'),
    ('article', 'adv', 'adj', 'noun'),
    ('adv', 'verb', 'article', 'noun')
)

WORDS_BY_TYPE = {}
_base_path = os.path.dirname(__file__)

for wtype in WORD_TYPES:
    with open(os.path.join(_base_path, '%s.txt' % wtype), 'r') as f:
        WORDS_BY_TYPE[wtype] = [w.strip() for w in f.readlines()]


def bytes_to_int(b1, b2, b3, b4):
    return (b1 << 24) | (b2 << 16) | (b3 << 8) | b4

def get_slots(input_str):
    # Turn unicode into a byte string if that's what we got.
    if isinstance(input_str, unicode):
        input_str = input_str.encode('UTF-8')

    md5 = hashlib.md5()
    md5.update(input_str)
    digest = [ord(b) for b in md5.digest()]

    return (
        bytes_to_int(*digest[0:4]),
        bytes_to_int(*digest[4:8]),
        bytes_to_int(*digest[8:12]),
        bytes_to_int(*digest[12:16]),
    )

def tripphrase(input_str):
    slots = get_slots(input_str)
    template = TEMPLATES[slots[3] % len(TEMPLATES)]


    words = []
    for idx, wtype in enumerate(template):
        options = WORDS_BY_TYPE[wtype]
        words.append(options[slots[idx] % len(options)])

    return ' '.join(words)

if __name__ == '__main__':
    import sys
    print tripphrase(sys.argv[1])
    sys.exit(0)

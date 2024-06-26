import re

_no_period_re = re.compile(r'(No[.])(?=[ ]?[0-9])')
_percent_re = re.compile(r'([ ]?[%])')
_half_re = re.compile('([0-9]½)|(½)')


# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
    ('X', 'ks'),
    ('x', 'ks'),
    ('sh', 'sz'),
    ('Sh', 'sz'),
    ('Th', 't'),
    ('th', 't'),
    ('kh', 'k'),
    ('Kh', 'k'),
    ('Lee', 'li'),
    ('lee', 'li'),
    ('cor', 'kor'),
    ('Cor', 'Kor'),
    ('V', 'w'),
    ('v', 'w'),
    ('innos', 'inos'),
    ('Innos', 'inos'),
]]


def _expand_no_period(m):
    word = m.group(0)
    if word[0] == 'N':
        return 'Number'
    return 'number'


def _expand_percent(m):
    return ' percent'


def _expand_half(m):
    word = m.group(1)
    if word is None:
        return 'half'
    return word[0] + ' and a half'


def normalize_abbreviations(text):
    text = re.sub(_no_period_re, _expand_no_period, text)
    text = re.sub(_percent_re, _expand_percent, text)
    text = re.sub(_half_re, _expand_half, text)
    return text

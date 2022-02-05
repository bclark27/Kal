import ply.lex as _lex
import dateutil.parser

states = (
    ('event', 'exclusive'),
    ('times', 'exclusive'),
    ('params', 'exclusive'),
)

tokens = (
    'DAY_OF_MONTH',
    'DAY_OF_WEEK',
    'MONTH',
    'DASH',
    'UNION',
    'SEPARATOR',
    'OF',
    'TIME',
    'ORDINAL',
    'EVENT',
)

t_times_DAY_OF_MONTH = r'\d\d?'
t_times_DAY_OF_WEEK = r'mon(day)?|tues(day)?|wed(nesday)?|thur(s(day)?)?|fri(day)?|sat(urday)?|sun(day)?'
t_times_MONTH = r'jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|june?|july?|aug(ust)?|sep(t(ember)?)?|oct(ober)?|nov(ember)?|dec(ember)?'
t_times_DASH = r'-'
t_times_UNION = r','

reserved = {
    'of': 'OF'
}

def t_ANY_SEPARATOR(t):
    r'//+'
    if t.lexer.lexstate == 'event':
        t.lexer.begin('times')
    elif t.lexer.lexstate == 'times':
        t.lexer.begin('params')
    return t


def t_event_EVENT(t):
    r'((?!//|\#\#).)+'
    t.value = str(t.value).strip()
    if t.value.startswith("==") and t.value.endswith("=="):
        t.lexer.header = t.value[2:-2].strip()
        return
    if res := reserved.get(t.value):
        t.type = res
    else:
        t.value = (t.value, lexer.header)
    return t


def t_times_TIME(t):
    r'\d\d?(:\d\d)?\ ?(am|pm)|\d\d:\d\d|midnight|noon'
    text = str(t.value).lower()
    if text == 'midnight':
        text = '00:00'
    elif text == 'noon':
        text = '12:00'
    t.value = dateutil.parser.parse(text).time()
    return t


def t_times_ORDINAL(t):
    r'1st|(2nd|second)( to last)?|3rd|4th|5th|first|third|fourth|fifth|last'
    text = str(t.value).lower()

    # parse an integer plus 2 chars
    first_char = text[0]
    if len(text) == 3 and first_char.isdigit():
        t.value = int(first_char)
        return t

    # parse the english instead
    ord_array = ("first", "second", "third", "fourth", "fifth")
    try:
        t.value = ord_array.index(text) + 1
        return t
    except ValueError:
        pass

    # special cases
    if text == 'last':
        t.value = -1
    else:
    # elif text == '2nd to last' or text == 'second to last':
        t.value = -2
    return t


# count the newlines so a) they are not illegal, and b) so the lexer knows which line it's on
def t_ANY_newline(t):
    r'(\r?\n)+'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('event')


def t_ANY_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


t_ANY_ignore_WHITESPACE = '\ \t'
t_ANY_ignore_COMMENT = r'\#\#.*'

lexer = _lex.lex()
lexer.begin('event')
lexer.header = ''

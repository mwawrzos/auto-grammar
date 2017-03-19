from ply import lex

tokens = ['WORD']

literals = '.,;–-!?:[]()"\''

t_ignore = r'  '

t_WORD = '(\w|-)+'


def t_error(t):
    raise Exception('Unknown token %s' % t)


lexer = lex.lex()

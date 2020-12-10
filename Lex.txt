import ply.lex as lex

reserved = { 'cdr': 'CDR', 'car': 'CAR' , 'let' : 'LET', 'cons': 'CONS'}

tokens = ['VAR','INT','LPAREN','RPAREN','PLUS','MINUS','TIMES','DIV', 'SEMI'] + \
  list(reserved.values())
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_SEMI = r';'
t_INT =r'[-+]?[0-9]+(\.([0-9]+)?)?'
t_CAR = r'[cC][Aa][rR]'
t_CDR = r'[cC][dD][rR]'
t_LET = r'[lL][eE][tT]'

def t_VAR(t):
  r'[a-zA-Z][_a-zA-Z0-9]*'
  t.type = reserved.get(t.value.lower(),'VAR')
  return t

#
#def t_LET(t):
##  r'let\(.*\)E'
 # t.type = reserved.get(t.value.lower(),'ID')
 # return t

# Ignored characters
t_ignore = " \r\n\t"
t_ignore_COMMENT = r'\#.*'

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  #t.lexer.skip(1)
  raise Exception('LEXER ERROR')
lexer = lex.lex()
## Test it out

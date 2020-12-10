import ply.yacc as yacc
from LispLexer import tokens

def p_lispStart(p):
  'lispStart : lisp SEMI'
  p[0] = ['lisp',p[1]]
def p_lispStart_1(p):
  'lispStart : list SEMI'
  p[0] = ['list',p[1]]


def p_lisp_1(p):
  'lisp : INT'
  p[0] = ['num',float(p[1])]
def p_lisp_2(p):
  'lisp : VAR'
  p[0] = ['var',p[1]]
def p_lisp_3(p):
  'lisp : LPAREN PLUS lisp lisp RPAREN'
  p[0] = ['+',p[3],p[4]]
def p_lisp_4(p):
  'lisp : LPAREN MINUS lisp lisp RPAREN'
  p[0] = ['-',p[3],p[4]]
def p_lisp_5(p):
  'lisp : LPAREN TIMES lisp lisp RPAREN'
  p[0] = ['*',p[3],p[4]]
def p_lisp_6(p):
  'lisp : LPAREN DIV lisp lisp RPAREN'
  p[0] = ['/',p[3],p[4]]
def p_lisp_7(p):
  'lisp : LPAREN CAR list RPAREN'
  p[0] = ['CAR']+[p[3]]
def p_lisp_8(p):
  'lisp : LPAREN LET LPAREN varlist RPAREN lisp RPAREN'
  p[0] = ['LET',p[4],p[6]]


def p_varlist(p):
    'varlist : LPAREN VAR lisp RPAREN'
    p[0] = [[p[2],p[3]]]
def p_varlist_1(p):
    'varlist : LPAREN VAR lisp RPAREN varlist'
    p[0] = [ [p[2],p[3] ]] + p[5]

def p_list_1(p):
    'list : LPAREN CDR list RPAREN'
    p[0] = [ 'CDR' , p[3]]
def p_list_2(p):
    'list : LPAREN seq RPAREN'
    p[0]=p[2]
def p_list_3(p):
    'list : LPAREN CONS lisp list RPAREN'
    p[0] = 'CONS',[p[3]]+p[4]

def p_seq_1(p):
    'seq : '
    p[0]=[]
def p_seq_2(p):
    'seq : lisp seq'
    p[0]=[p[1],p[2]]

def p_error(p):
  raise Exception('SYNTAX ERROR')

parser = yacc.yacc()

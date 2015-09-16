import ply.lex as lex
import ply.yacc as yacc

tokens = (
"DASH",
"INPUT",
"SQUARECLOSE",
"SQUAREOPEN",
"ROUNDCLOSE",
"ROUNDOPEN",
"NEWLINE",
"TERMINATOR"
)

# Regex for tokens
t_SQUAREOPEN     = r'\['
t_SQUARECLOSE   = r'\]'
t_ROUNDOPEN     = r'\('
t_ROUNDCLOSE   = r'\)'
#t_INPUT = r'no'             ## For Debugging, start with a deterministic string
t_DASH = r'\-'
t_INPUT = r'[a-zA-Z_0-9]+'  
t_TERMINATOR = r';'
t_ignore    = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Parsing rules

def p_expression_create(p):
    '''expression : ROUNDOPEN INPUT ROUNDCLOSE DASH SQUAREOPEN INPUT SQUARECLOSE DASH ROUNDOPEN INPUT ROUNDCLOSE TERMINATOR
	| ROUNDOPEN INPUT ROUNDCLOSE TERMINATOR'''
    if p[4] == "-" : print "Edge ", p[6], "is created for the nodes ", p[2], "and ", p[10]
    elif p[4] == ";" : print "Node ", p[2], " is created"

def p_statement(p):
    '''statement : expression'''
    print p[0] 
	
def p_error(p):
    print("Syntax error at '%s'" % repr(p)) #p.value)

yacc.yacc()

while True:
    try:
        input = raw_input('cypher> ')
    except EOFError:
        print "End of line"	
        break
    yacc.parse(input)
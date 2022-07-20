class Class(Enum):
    operadores={
    '+':"plus",
    '-':"minus",
    ',': "comma",
    '*':"star",
    '/':"fwslash",
    '=':'eq',
    '==': "assign",
    '<':"lt",
    '>':"gt",
    '%':"percent"
}

    dictDelim={
    '(':"LPAREN",
    ')':"RPAREN",
    '{':"LBRACKET",
    '}':"RBRACKET",
   
}

    statementList={ #palabra reservada
    "if":"IF",
    "while":"WHILE",
    "int":"INT",
    'string':"STRING",
    'char':"CHAR",
    'print:"PRINT",
    'EOF': "eof",
        
}
  
class Token:
    def __init__(self,nombre,valor):
        self.nombre= nombre
        self.valor = valor
    def getType(self):
        return self.nombre
    def getValue(self):
        return self.valor
    def __repr__(self):
        return f"<{self.nombre},{self.valor}>"

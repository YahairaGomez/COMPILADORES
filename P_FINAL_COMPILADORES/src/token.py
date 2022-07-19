from enum import Enum, auto


class Class(Enum):
    PLUS = auto()
    MINUS = auto()
    FWDSLASH = auto()
    PERCENT = auto()

    EQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()

    ASSIGN = auto()
    SEMICOLON = auto()
    COMMA = auto()

    TYPE = auto()
    INT = auto()
    CHAR = auto()
    STRING = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()
    
    ID = auto()
    EOF = auto()



class Token:
    def __init__(self, class_, lexeme):
        self.class_ = class_
        self.lexeme = lexeme

    def __str__(self):
        return "<{} {}>".format(self.class_, self.lexeme)
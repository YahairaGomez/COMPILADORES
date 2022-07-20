import string
from Tokens import Token
from Sintactico import parseTree
from Sintactico import Sintactico
digitos="0123456789"
letras=string.ascii_letters
letrasDigitos=letras+digitos
"Analizador Lexico"
operadores={
    '+':"OP_SUM",
    '-':"OP_RES",
    '.':"PUNTO",
    ',': "COMA",
    '*':"OP_MULTI",
    '/':"OP_DIV",
    ':=':"ASSIGN",
    '=':'EQUAL',
    '!=':"DIFFERENT",
    '<':"MENOR",
    '>':"MAYOR"
}

dictDelim={
    '(':"PARENTESIS_IZQ",
    ')':"PARENTESIS_DER",
    '{':"LLAVE_INI",
    '}':"LLAVE_FIN",
   
}
statementList={ #palabra reservada
    "if":"IF",
    "while":"WHILE",
    "integer":"INTEGER",
    'int':"INT",
    'string':"STRING",
    'print:"PRINT"'
    'read:"READ"'
    'float':"FLOAT",
    'Write':"WRITE",
    "var":"VAR",
}
charEvitar=['\t',' ','\n']
###################################################################################
class AnalizadorLexico:
    def __init__(self,text):
        self.text=text
        self.puntero=-1
        self.tokens=[]
        self.crearTokens()
        self.getTokens()
    def getChar(self):
        self.puntero+=1
        if self.puntero < (len(self.text)):
            return self.text[self.puntero]
        return None
    def peekChar(self):
        if self.puntero<(len(self.text)-1):
            return self.text[self.puntero+1]
        return None
    def peek2Char(self):
        if self.puntero<(len(self.text)-1):
            return self.text[self.puntero+2]
        return None
    def getTokens(self):
        for token in self.tokens:
            print(repr(token))  
    def crearNumero(self):
        numeroString=""
        charActual=self.getChar()
        numeroString+=charActual
        #print(f"numero{numeroString} siguiente:\"{self.peekChar()}\"")
        while (self.peekChar()not in charEvitar) and self.peekChar()!=';':
            charActual=self.getChar()    
            #print(f"char actual: \"{charActual}\"")
            numeroString+=charActual

        self.puntero+=1

        if numeroString.find(".") == -1:
            tipoNumero= False
            
        else:
            tipoNumero= True
      
        if tipoNumero == True :
            try:
                float(numeroString) #convertir a float
            except:
                print(f"Error: Numero incorrecto {numeroString}")
            else:
                self.tokens.append( Token("NUM",numeroString))
        else:
            try:
                if len(numeroString)> 10:
                    print("Error:Muy grande")
                    return
                else:
                    int(numeroString) #convertir a int
            except:
                print(f"Error: Numero incorrecto {numeroString}")
            else:
                self.tokens.append( Token("NUM",numeroString))

    def crearIdentificador(self):
        identificadorString=""
        charActual=self.getChar()
        identificadorString+=charActual
        while self.peekChar() != None and self.peekChar() in letrasDigitos + '_':
            charActual=self.getChar()
            identificadorString+=charActual
        if identificadorString in statementList:
            self.tokens.append(Token(statementList[identificadorString],identificadorString))
            return
        self.tokens.append(Token("ID",identificadorString))
    def crearTokens(self):
        while self.peekChar()!=None:
            if self.peekChar() in charEvitar:
                self.puntero+=1
            elif self.peekChar() in digitos:
                self.crearNumero()
            elif self.peekChar() in letras:
                self.crearIdentificador()
            
            elif self.peekChar()=='/' and self.peek2Char()=='*' :
                #self.puntero+=1
                while True:
                    if self.peekChar()=='*' and self.peek2Char()=='/' :
                        print("<COMENTARIO>")
                        self.puntero+=2
                        break
                    self.puntero+=1
            elif self.peekChar() in dictDelim:
                charDelim=self.getChar()
                self.tokens.append(Token(dictDelim[charDelim],charDelim))
            elif self.peekChar() in operadores:
                charDeOpera=self.getChar()
                self.tokens.append(Token(operadores[charDeOpera],charDeOpera))
            elif self.peekChar()==':':
                Signo=self.getChar()
                if self.peekChar() !=None and self.peekChar()=='=':
                    Signo+=self.getChar()
                    self.tokens.append(Token("ASSIGN",Signo))
                else:
                    self.tokens.append(Token("DOS_PUNTOS",Signo))
            elif self.peekChar()=='\'':
                self.puntero+=1
                contenidoString=self.getChar()
                while self.peekChar() != None and self.peekChar()!='\'':
                    contenidoString+=self.getChar()
                self.puntero+=1
                self.tokens.append(Token("STR",contenidoString))


            else:
                print(f"Error: Caracter invalido \'{self.getChar()}\'")

###################################################################################
if __name__ == "__main__":
    codigoTxt=open("main.txt","r")
    analizador=AnalizadorLexico(codigoTxt.read())
    codigoTxt.close()
    list_tokens=analizador.tokens
    
#2da parte
    analizadorsintatico=Sintactico()
    analizadorsintatico.analizador(list_tokens)
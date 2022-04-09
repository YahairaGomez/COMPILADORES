
# LEXER: CONVIERTE EL INPUT DIGITO A DIGITO Y CONVIERTE ESTE INPUT EN TOKENS
# EJM: TOKENS [INT:3, PLUS, INT:5]
#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'

# ERRORS

class Error:
    # Nombre del error y detalles
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        # Imprime el nombre de error y detalles
        result  = f'{self.error_name}: {self.details}\n'
        #result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    # Errores inválidos
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# TOKENS

type_integer = 'INT'
type_float   = 'FLOAT'
plus_op      = 'PLUS'
minus_op     = 'MINUS'
mul_op       = 'MUL'
div_op       = 'DIV'
Left_parenth = 'LPAREN'
Right_parenth= 'RPAREN'

# Clase Token que tiene tipo de token y valor
class Token:
    #CONSTRUCTOR
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    #METODO DE REPRESENTACION: [INT:12]
    def __repr__(self):
        #Si el token tiene el valor 
        if self.value: 
            #Imprimo el tipo : valor
            return f'{self.type}:{self.value}'

        #Si no tiene valor, solo imprimo el tipo
        return f'{self.type}'



# LEXER


class Lexer:
    # Voy a tener el text que voy a procesar
    #Tengo que guardar la posicion y caracter actual 
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        #-1 Porque Advance incrementa apenas es llamado
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    #Avanza hacia el siguiente caracter en el text
    def advance(self):
        self.pos.advance(self.current_char)
        #Avanzo a la sgte posicion solo si no acabe de recorrer el texto entero 
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        # Ayuda a advance
        # Lista vacia donde guardaré los valores 
        tokens = []

        #Evalúo caracter por caracter y contruyo mi string de tokens
        while self.current_char != None:
            # Espacios, tabs --> Solo avanzo
            if self.current_char in ' \t':
                self.advance()

            # Checho si está es la lista DIGITS
            # OJO: Como los números pueden tener más de 1 digit o ser flotantes, hago uso de funcion make_number
            # Make_number crea tokens tipo int o float    
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            # CASO SIGNOS!! SOLO AGREGO DICHO SIMBOLO A MI LISTA
            elif self.current_char == '+':
                tokens.append(Token(plus_op))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(minus_op))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(mul_op))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(div_op))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Left_parenth))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Right_parenth))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        # Retorna tokens si está bien y None si está mal
        return tokens, None

    def make_number(self):
        # Mi numero es un string 
        num_str = ''

        # Para checar si es float o int
        # Si dot_count = 0 --> int
        # Sino --> float e indico cuantos decimales tiene
        dot_count = 0

        # Evaluo todo mi string y checo que el caracter analizado siga siendo un Digito o un punto
        while self.current_char != None and self.current_char in DIGITS + '.':
            # Si encuentro un punto --> es flotante
            # dot_count aumenta para checar cuantos decimales tiene
            if self.current_char == '.':
                # Salgo de bucle, porque no pueden haber 2 puntos en un número
                if dot_count == 1: break
                dot_count += 1
                # Añado el punto num_str y luego sigo con el else de linea 168
                # hasta pasar todo el numero
                num_str += '.'
            else:
                # Añado a num_str hasta que encuentre el punto
                # lo añado y creo el nuevo número
                num_str += self.current_char
            self.advance()

        # CASTING
        if dot_count == 0:
            return Token(type_integer, int(num_str))
        else:
            return Token(type_float, float(num_str))

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
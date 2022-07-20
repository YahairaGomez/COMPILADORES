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










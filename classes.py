class Token:
    def __init__(self, funcao, id):
        self.funcao = funcao
        self.id = id

class Simbolo:
    def __init__(self,id,posicao,linha,coluna):
        self.id = id
        self.posicao = posicao
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        return "[{}, {}, ({}, {})]".format(self.id, "" if self.posicao==None else self.posicao, self.linha, self.coluna)

class Dicionario:
    def __init__(self):
        self.lista = []
        self.lista.append(Token("rem",61))
        self.lista.append(Token("input",62))
        self.lista.append(Token("let",63))
        self.lista.append(Token("print",64))
        self.lista.append(Token("goto",65))
        self.lista.append(Token("if",66))
        self.lista.append(Token("end",67))
        self.lista.append(Token("=",11))
        self.lista.append(Token("+",21))
        self.lista.append(Token("-",22))
        self.lista.append(Token("*",23))
        self.lista.append(Token("/",24))
        self.lista.append(Token("%",25))
        self.lista.append(Token("==",31))
        self.lista.append(Token("!=",32))
        self.lista.append(Token(">",33))
        self.lista.append(Token("<",34))
        self.lista.append(Token(">=",35))
        self.lista.append(Token("<=",36))

        self.lista.append(Token("LF",10))
        self.lista.append(Token("ETX",3))
        self.lista.append(Token("var",41))
        self.lista.append(Token("const",51))

    def token(self,txt):
        for item in self.lista:
            if item.funcao==txt:
                return item
        return Token("",0)

    def token_existe(self,txt):
        for item in self.lista:
            if item.funcao==txt or (txt.isnumeric() and int(txt)==item.id):
                return True
        return False
from argparse import ArgumentParser
import re

#Classes
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
            if item.funcao==txt or (txt.isnumeric() and int(txt)==item.id):
                return item
        return Token("",0)

    def token_existe(self,txt):
        for item in self.lista:
            if item.funcao==txt or (txt.isnumeric() and int(txt)==item.id):
                return True
        return False
    

#Funções úteis..
def remover_espacos_duplos(txt):
    while "  " in txt:
        txt = re.sub('[ ]{2,}'," ",txt)
    
    return txt

def prepara_linha(linha):
    if linha=="":
        return ""

    linha = remover_espacos_duplos(linha)

    if linha[0]==" ":
        linha = linha[1:]
    if linha[-1]==" ":        
        linha = linha[0:-1]

    return linha + " "

def adiciona_se_nao_existe(var,txt):
    if txt in var:
        return var.index(txt)
    else:
        var.append(txt)
        return len(var)-1
    return -1

#Lê o nome o arquivo e coloca na variavel args.filename
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="compile FILE", metavar="FILE")
args = parser.parse_args()

#Início do compilador
dicionario = Dicionario()
memoria = []
resultado = []
erros = []
numero_linha = 0

file = open(args.filename)
linhas = file.read().split('\n') #Lê o arquivo e transforma em uma array com as quebras de linha

for linha in range(1,len(linhas)+1):
    conteudo = linhas[linha-1]

    if conteudo=="":
        continue

    conteudo = prepara_linha(conteudo)
    buffer = ""
    comentario = False

    for coluna in range(1,len(conteudo)+1):
        c = conteudo[coluna-1]
        
        #Checa se tem uma letra em um comando numérico
        if buffer!="" and c!=" " and buffer[0].isnumeric() and not comentario:
            if not c.isnumeric():
                erros.append("Caractér não identificado na linha {}, coluna {}".format(linha,coluna))
                continue

        if not comentario:
            if c != " ":
                buffer += c
            else:
                if len(buffer)==coluna-1:
                    if not buffer.isnumeric():
                        erros.append("Número da linha {} não definido".format(linha))
                    else:
                        if numero_linha > int(buffer):
                            erros.append("Id da linha {} é maior do que o anterior".format(linha))

                        numero_linha = int(buffer)
                        
                        indice = adiciona_se_nao_existe(memoria, buffer)
                        resultado.append(Simbolo(51, indice, linha, coluna-len(buffer)))
                else:
                    t = dicionario.token(buffer)

                    if t.id==0:
                        if buffer.isnumeric():
                            resultado.append(Simbolo(51, None, linha, coluna-len(buffer)))
                        else:
                            indice = adiciona_se_nao_existe(memoria, buffer)
                            resultado.append(Simbolo(41, indice, linha, coluna-len(buffer)))
                    else:
                        resultado.append(Simbolo(t.id, None, linha, coluna-len(buffer)))
                        if t.id==61:
                            comentario=True
                buffer = ""

        if coluna==len(conteudo):
            if linha==len(linhas):
                resultado.append(Simbolo(3, None, linha, coluna))
            else:
                resultado.append(Simbolo(10, None, linha, coluna))

#print(erros)
for simbolo in resultado:
    print(simbolo)


            

    


from functions import prepara_linha, adiciona_se_nao_existe
from classes import Token,Simbolo
from re import match

class Compilador_Lexico:
    def __init__(self,dicionario):
        self._memoria = []
        self._resultado = []
        self._erros = []
        self._numero_linha = 0
        self._dicionario = dicionario

    def abre_arquivo(self,arquivo):
        self.arquivo = open(arquivo)

    def __str__(self):
        retorno = ""

        for simbolo in self._resultado:
            retorno = retorno + str(simbolo) + " "

        return retorno

    def resultado(self):
        return self._resultado

    def memoria(self):
        return self._memoria

    def get_erros(self):
        return self._erros

    def processa(self):
        linhas = self.arquivo.read().split('\n') #Lê o arquivo e transforma em uma array com as quebras de linha
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
                        self._erros.append("Caractér não identificado na linha {}, coluna {}".format(linha,coluna))
                        continue

                if not comentario:
                    if c != " ":
                        buffer += c
                    else:
                        if not buffer.isnumeric() and match("[a-z]*[A-Z]+[a-z]*",buffer)!=None:
                            self._erros.append("Erro Léxico: Letra maíuscula encontrada na linha {}".format(linha))
                        elif len(buffer)==coluna-1:
                            if not buffer.isnumeric():
                                self._erros.append("Número da linha {} não definido".format(linha))
                            else:
                                if self._numero_linha > int(buffer):
                                    self._erros.append("Erro Semântico: Rótulo da linha {} é menor do que o anterior".format(linha))

                                self._numero_linha = int(buffer)
                                
                                indice = adiciona_se_nao_existe(self._memoria, buffer)
                                self._resultado.append(Simbolo(51, indice, linha, coluna-len(buffer), int(buffer)))
                        else:
                            t = self._dicionario.token(buffer)

                            if t.id==0:
                                if buffer.isnumeric():
                                    self._resultado.append(Simbolo(51, None, linha, coluna-len(buffer), int(buffer)))
                                else:
                                    if len(buffer)!=1:
                                        self._erros.append("Variável com mais de 1 caracter na linha {}, coluna {}".format(linha,coluna))

                                    indice = adiciona_se_nao_existe(self._memoria, buffer)
                                    self._resultado.append(Simbolo(41, indice, linha, coluna-len(buffer), None))
                            else:
                                self._resultado.append(Simbolo(t.id, None, linha, coluna-len(buffer), None))
                                if t.id==61:
                                    comentario=True
                        buffer = ""

                if coluna==len(conteudo):
                    if linha==len(linhas):
                        self._resultado.append(Simbolo(3, None, linha, coluna, None))
                    else:
                        self._resultado.append(Simbolo(10, None, linha, coluna, None))


            

    


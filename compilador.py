from argparse import ArgumentParser
import classes
import functions

#Lê o nome o arquivo e coloca na variavel args.filename
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="compile FILE", metavar="FILE")
args = parser.parse_args()

#Início do compilador
dicionario = classes.Dicionario()
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

    conteudo = functions.prepara_linha(conteudo)
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
                        
                        indice = functions.adiciona_se_nao_existe(memoria, buffer)
                        resultado.append(classes.Simbolo(51, indice, linha, coluna-len(buffer)))
                else:
                    t = dicionario.token(buffer)

                    if t.id==0:
                        if buffer.isnumeric():
                            resultado.append(classes.Simbolo(51, None, linha, coluna-len(buffer)))
                        else:
                            indice = functions.adiciona_se_nao_existe(memoria, buffer)
                            resultado.append(classes.Simbolo(41, indice, linha, coluna-len(buffer)))
                    else:
                        resultado.append(classes.Simbolo(t.id, None, linha, coluna-len(buffer)))
                        if t.id==61:
                            comentario=True
                buffer = ""

        if coluna==len(conteudo):
            if linha==len(linhas):
                resultado.append(classes.Simbolo(3, None, linha, coluna))
            else:
                resultado.append(classes.Simbolo(10, None, linha, coluna))

#print(erros)
for simbolo in resultado:
    print(simbolo)


            

    


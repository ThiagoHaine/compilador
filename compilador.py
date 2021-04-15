from argparse import ArgumentParser
from classes import Dicionario
from compilador_lexico import Compilador_Lexico
from compilador_sintatico import Compilador_Sintatico
import functions

#Lê o nome o arquivo e coloca na variavel args.filename
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="compile FILE", metavar="FILE")
args = parser.parse_args()

dicionario = Dicionario()
lexico = Compilador_Lexico(dicionario)

lexico.abre_arquivo(args.filename)
lexico.processa()

#print(lexico)
print(lexico.erros)

sintatico = Compilador_Sintatico(lexico.resultado())
sintatico.processa()

print(sintatico.getErros())
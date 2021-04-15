from argparse import ArgumentParser
from classes import Dicionario
from compilador_lexico import Compilador_Lexico
from compilador_sintatico import Compilador_Sintatico
import functions

erros = []

#Lê o nome o arquivo e coloca na variavel args.filename
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="compile FILE", metavar="FILE")
args = parser.parse_args()

dicionario = Dicionario()

#Compilador Léxico
lexico = Compilador_Lexico(dicionario)
lexico.abre_arquivo(args.filename)
lexico.processa()

#Compilador Sintático
sintatico = Compilador_Sintatico(lexico.resultado(), lexico.memoria())
sintatico.processa()

erros = erros + lexico.get_erros() + sintatico.get_erros()

if len(erros)==0:
    print("Nenhum erro encontrado no arquivo de entrada")
else:
    print("Erros detectados: ")
    for erro in range(0,len(erros)):
        print("{} - {}".format(erro+1, erros[erro]))
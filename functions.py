import re
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
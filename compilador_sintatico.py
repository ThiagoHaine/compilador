from classes import Simbolo

class Compilador_Sintatico:
    def __init__(self, resultado_lexico):
        self._resultado_lexico = resultado_lexico
        self._erros = []
        self._token = 0

    def _atrib(self):
        self.next_token()
        if self._token.id!=11:
            self.erro("Erro: = esperado em {},{}",self._token)
            
    def _var(self):
        self.next_token()
        if self._token.id!=41:
            self.erro("Erro: Variável esperada em {},{}",self._token)

    def _num_or_var(self):
        self.next_token()
        if self._token.id!=51 and self._token.id!=41:
            self.erro("Erro: Variável ou constante numérica esperada em {},{}",self._token)

    def _num(self):
        self.next_token()
        if self._token.id!=51:
            self.erro("Erro: Constante numérica esperada em {},{}",self._token)

    def _operador(self):
        self.next_token()
        if self._token.id<21 or self._token.id>25:
            self.erro("Erro: Operador aritmético esperado em {},{}",self._token)

    def _operador_rel(self):
        self.next_token()
        if self._token.id<31 or self._token.id>36:
            self.erro("Erro: Operador relacional esperado em {},{}",self._token)        

    def _lf(self):
        self.next_token()
        if (self._token.id!=10 and self._token.id!=3):
            self.erro("Erro: Fim de linha esperado em {},{}",self._token)        

    def _num_linha(self):
        self.next_token()
        if (self._token.id!=51):
            self.erro("Erro: Número da linha esperado em {},{}",self._token)

    def _palavra_reservada(self):
        self.next_token()
        if self._token.id>60 and self._token.id<68:
            if (self._token.id==61):
                self._lf()
            elif (self._token.id==62):
                self._var()
                self._lf()
            elif (self._token.id==63):
                self._var()
                self._atrib()
                self._num_or_var()

                while(self._resultado_lexico[0].id!=10 and self._resultado_lexico[0].id!=3):
                    self._operador()
                    self._num_or_var()

                self._lf()
            elif (self._token.id==64):
                self._num_or_var()
                self._lf()
            elif (self._token.id==65):
                self._num()
                self._lf()
            elif (self._token.id==66):
                self._num_or_var()
                self._operador_rel()
                self._num_or_var()
                self._palavra_reservada()
            elif (self._token.id==67):
                self._lf()
        else:
            self.erro("Erro: Palavra reservada esperada em {},{}",self._token)

    def next_token(self):
        self._token = self._resultado_lexico.pop(0)
        
    def erro(self,err,token):
        self._erros.append(err.format(token.linha,token.coluna))

    def processa(self):
        self._num_linha()
        self._palavra_reservada()

        while(self._token.id!=10 and self._token.id!=3):
            self.next_token()

        if len(self._resultado_lexico)!=0:
            self.processa()

    def getErros(self):
        return self._erros
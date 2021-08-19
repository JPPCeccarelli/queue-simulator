#Aluno: João Pedro do Patrocinio Ceccarelli
#Numero USP: 8932154

import math

class Cliente():
    def __init__(self,clienteid, tipoEvento,timeEvento1):
        self.__clienteid = clienteid
        self.__tipoEvento = tipoEvento   # tipo do evento que sera' o
                                         # proximo a ocorrer
        self.__timeEvento1 = timeEvento1 # instante de tempo de ocorrencia
                                         # do Evento 1
        self.__timeEvento2 = 0        # idem Evento 2
        self.__timeEvento3 = 0        # idem Evento 3
        self.__caixaid = 0            # identificacao do caixa
        
    def set_clienteid(self,clienteid):
        self.__clienteid = clienteid
    def get_clienteid(self):
        return(self.__clienteid)

    def set_tipoEvento(self,tipo):
        if tipo in range(1,4):        
           self.__tipoEvento = tipo
        else:
            print('Tipo de evento não existente')
            
    def get_tipoEvento(self):
        return(self.__tipoEvento)
        
    def set_timeEvento(self,time,tipoevento):
        if tipoevento == 1:
            self.__timeEvento1 = time
        else:
            if tipoevento == 2:
                self.__timeEvento2 = time
            else:
                if tipoevento == 3:
                    self.__timeEvento3 = time
                else:
                    print("Evento nao identificado!!!")
                    
    def get_timeEvento(self,tipoevento):
        if tipoevento == 1:
            return(self.__timeEvento1)
        else:
            if tipoevento == 2:
                return(self.__timeEvento2)
            else:
                if tipoevento == 3:
                    return(self.__timeEvento3)
                else:
                    print("Evento nao identificado!!!")
                    
    def set_caixaid(self,caixaid):
        self.__caixaid = caixaid
    def get_caixaid(self):
        x=self.__caixaid
        return(x)
        
    def __lt__(self, other):
        return self.__clienteid < other.__clienteid

    def __str__(self):
        x = "clienteid = " + str(self.__clienteid) + "\n" + \
             "tipoEvento  = " + str(self.__tipoEvento)  + "\n" + \
            "timeEvento1 = " + str(self.__timeEvento1) + "\n" + \
            "timeEvento2 = " + str(self.__timeEvento2) + "\n" + \
            "timeEvento3 = " + str(self.__timeEvento3) + "\n" + \
            "Caixa ID = " + str(self.__caixaid) + "\n\n"
        return(x)

# FIFO
class FilaCaixa():
    def __init__(self):
        self.__fila = []
        
    #corrigir isso depois
    def insereFilaCaixa(self, cliente):
        self.__fila.append(cliente)
        
    def retiraFilaCaixa(self):
        return self.__fila.pop(0)
    
    def FilaCaixaEstaVazia(self):
        if len(self.__fila) == 0:
            return True
        else:
            return False
        
    def tamFila(self):
        return len(self.__fila)
            
#foi feito exatamente igual ao pedido no Lab 7 (28/05)        
class No:       # Classe que armazena o conteÃºdo
    def __init__(self, data):
        self.data = data 
        self.next = None
    
class FilaEventos:      
    def __init__(self):  # Inicializacao da fila
                         # Ponteiros inicio=fim=None
        self.inicio = None
        self.fim = None       
  
    def FilaEventosVazia(self):  # Checa se a fila esta vazia
        return(self.inicio == None) # basta testar um ponteiro
      
    def insereFilaEventos(self, item): 
        temp = No(item)       # Cria um objeto No que passa a
                              # armazenar item
        if self.fim == None:  # Se a fila esta vazia entao
                              # os dois ponteiros apontam para o mesmo No
            self.inicio = temp
            self.fim = temp
        else: 
            self.fim.next = temp 
            self.fim = temp 
   
    def retiraFilaEventos(self):                        #algoritmo do tipo insertion sort
        atual = self.inicio                             #cria variável que aponta para o inicio
        while(atual != None):                           #pára o loop quando 'atual' acabar
            aux = self.inicio.next                      #outra variável que aponta para o próximo valor de 'atual'
            while(aux != None):                         # 
                if(atual.data > aux.data):              #se o valor contido na posição de 'atual' da lista for maior que
                                                        #o valor de 'aux' então eles trocam de posição
                    atual.data, aux.data = aux.data, atual.data
                aux = aux.next                          #aponta para o próximo ponteiro de aux
            atual = atual.next                          #aponto para o proximo ponteiro de atual
        
        aux = None  
        if not self.FilaEventosVazia(): # Se a fila nao esta vazia
           temp = self.inicio
           aux = temp.data           # aux <-- data
           self.inicio = temp.next   # movimenta o ponteiro inicio
        if(self.inicio == None): # se a fila ficou vazia
            self.fim = None      # o ponteiro fim deve ser atualizado
        return(aux) # Se a fila estiver vazia retorna None
            
    
class ListaClientesSaida():
    def __init__(self):
        self.__filasaida=[]
        
    def insereListaSaida(self,cliente):
        self.__filasaida.append(cliente)
        
    def retiraListaSaida(self):
        return(self.__filasaida.pop(0))
        
    def ListaSaidaVazia(self):
        if len(self.__filasaida) == 0:
            return(True)
        else:
            return(False)
        
    def tamListaSaida(self):
        x=len(self.__filasaida)
        return(x)

#verifica se há caixa livre no array de entrada
def verificaCaixaLivre(sinalCaixaLivre):
    for i in range(len(sinalCaixaLivre)):
        if sinalCaixaLivre[i]:
            return True, i
    return False, -1
 
#encontra menor fila
#atualiza 'a' a cada valor menor encontrado
def achaMenorFila(vetorFilaCaixa):
    a = math.inf
    for i in range(len(vetorFilaCaixa)):
        if(vetorFilaCaixa[i].FilaCaixaEstaVazia()):
            return i
        if(vetorFilaCaixa[i].tamFila() < a):
            i_ret = i
            a = vetorFilaCaixa[i].tamFila()
    return i_ret
    
#retorna tamanho da fila para cada vetorFilaCaixa[i]
def TamanhoDasFilas(vetorFilaCaixa):
    return vetorFilaCaixa.tamFila()
        
    

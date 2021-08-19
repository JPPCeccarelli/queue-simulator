#Aluno: João Pedro do Patrocinio Ceccarelli
#Numero USP: 8932154

from statistics import *
import random as rand

#from Filas import *

#
# Gera amostras de intervalos de tempo entre chegada de clientes Dtev1
# Numero de amostras é compativel com a duracao do expediente
# - lambdacliente: taxa de chegada de clientes por segundo
# - duracaoexpediente: duracao de tempo do expediente da agencia bancaria
#   especificada em segundos 
def fexp(lambdacliente,duracaoexpediente):   
    x = 1000*[None]         # x e' alocado com 1000 posicoes
    somatoriadotempo = 0    # Somatoria dos intervalos de tempo Dtev1
    k=0
    # Amostras sao geradas ate' que a somatoria dos intervalos de tempo
    # ultrapasse a duracao do expediente
    while somatoriadotempo <= duracaoexpediente:    
        x[k] = rand.expovariate(lambdacliente)
        x[k] = int(x[k])
        somatoriadotempo = somatoriadotempo + x[k]
        k = k+1
    # retira-se o ultimo elemento que esta'alem do horario
    # do expediente                                                                                                                    
    return x[0:k-1]

#
# mucaixa: taxa de atendimento em segundos
# tempominimoatendimento: tempo minimo de atendimento em
# segundos
def TempoDeAtendimentoCaixa(mucaixa,tempominimoatendimento):
        x = int(rand.expovariate(mucaixa))
        if x >= tempominimoatendimento:
           return(x)
        else:
           return(tempominimoatendimento)

#
# Codigo que voce deve desenvolver
#
def calculaEstatisticas(listasaida,logfilas):
    #dados estatisticos usando as funções já prontas da biblioteca statistics
    tfm = mean(item[0] for item in listasaida[:])
    tcm = mean(item[1] for item in listasaida[:])
    ttm = mean(item[2] for item in listasaida[:])
    vf = variance(item[0] for item in listasaida[:])
    vc = variance(item[1] for item in listasaida[:])
    vt = variance(item[2] for item in listasaida[:])
    
    temp = 0
    #variavel que retorna o numero médio de clientes na fila
    n_medio = 0
    #contador de total de simulações
    cont = 0
    #calcula numero médio de clientes
    for i in range(1, len(logfilas)):
        #condição que verifica se os tempos são da mesma simulação
        if(logfilas[i][0] >= logfilas[i-1][0]):
            #aux soma todos os tamanhos de fila
            aux = 0
            for j in range(1, len(logfilas[0])):
                aux = logfilas[i][j] + aux
            #atualiza temp com a somatória de clientes em cada fila multiplicada pelo tempo em que a fila ficou assim
            temp = temp + aux*(logfilas[i][0]-logfilas[i-1][0])
        else:
            n_medio = temp/logfilas[i-1][0] + n_medio
            temp = 0
            cont += 1
            
    #itera mais uma vez pois para a última posição de logfilas
    #a condição não é requerida
    n_medio = temp/logfilas[len(logfilas)-1][0] + n_medio
    cont += 1
    
    #divide n_medio pelo total de simulações
    n_medio = n_medio/cont
            
    return tfm, tcm, ttm, vf, vc, vt, n_medio

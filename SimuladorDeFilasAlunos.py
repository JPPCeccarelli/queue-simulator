""" Aluno: João Pedro do Patrocinio Ceccarelli
 Número USP: 8932154
 OBS: para escolher qual simulação deverá ser plotada basta alterar a
 variável 'n_simulacao', na linha 8"""
 
# escolhe uma simulação específica para plotar o gráfico (de 0 até numeroderepeticoes-1)
# mudar o valor de n_simulacao para escolher outro plot
n_simulacao = 0

# Bibliotecas Python
import sys
from statistics import *
import matplotlib.pyplot as plt
import numpy as np

# Classes desenvolvidas para o Simulador de Filas
from AleatorioAlunos import *
from FilasAlunos import *
            
# definir aqui a funcao simulacao
def simulacao():
    
    #variavel auxiliar para plotagem do gráfico
    grafico_temp = []
    
    #coleta os intervalos de tempo obtidos com a distribuição de Poisson
    Dtev1 = fexp(lambdacliente_hour/3600,duracaoexpediente_hour*3600)
    nc = len(Dtev1)
    
    #lista de clientes
    todos_os_clientes = nc*[None]
    
    #t_abs é a somatória de Dtev[i], para já criar os eventos 1 no tempo absoluto
    t_abs = 0
    
    # todos os eventos <Evento1> são criados no inicio
    for i in range(nc):
        t_abs += Dtev1[i]
        
        #Criar <nc> eventos <Evento1> # criar objetos da classe <Cliente>
        todos_os_clientes[i] = Cliente(i, 1, t_abs)
        
        #Inserir eventos <Evento1> na fila de eventos <FE>
        FE.insereFilaEventos((t_abs, todos_os_clientes[i]))
        
    #Enquanto houver eventos em <FE> Faça    
    while FE.FilaEventosVazia() is False:
    #{ 
        ev_re = FE.retiraFilaEventos()
        #ev_re = evento retirado
        #ev_re[0] = clock
        #ev_re[1] = objeto cliente (<evento>)
        
        #Se <evento> for <Evento1> então
        if ev_re[1].get_tipoEvento() == 1:
        #{
            #return da funcao verificaCaixaLivre
            sinal_caixa, caixa_id = verificaCaixaLivre(sinalCaixaLivre)
            
            #Se existe(m) caixa(s) livre(s) Então
            if sinal_caixa:
            #{
                #escolhe um caixa livre identificado como <caixaid>
                ev_re[1].set_caixaid(caixa_id)
                
                #cria um Evento2 para o instante de tempo <clock> associado a <evento>
                ev_re[1].set_tipoEvento(2)
                ev_re[1].set_timeEvento(ev_re[0], 2)
                FE.insereFilaEventos((ev_re[1].get_timeEvento(2), ev_re[1]))
                
                #Sinaliza o caixa identificado por <caixaid> como ocupado
                sinalCaixaLivre[caixa_id] = False
                #}
            #Senão
            else:
            #{
                #Escolha uma fila de caixa mais curta
                mf = achaMenorFila(vetorFilaCaixa)
                
                #Insere <evento> na fila de caixa
                vetorFilaCaixa[mf].insereFilaCaixa(ev_re[1])
                
                #Loga o estado das filas em <logfilas>
                #temp = vetor temporario para armazenar tamanho da fila e clock
                temp = (nCaixas+1)*[None]
                temp[0] = ev_re[0]
                for i in range(nCaixas):
                    temp[i+1] = TamanhoDasFilas(vetorFilaCaixa[i])
                    
                #atualiza logfilas e o grafico
                logfilas.append(temp)
                grafico_temp.append(temp)
                #}
        #}
        #Senão Se <evento> for do tipo 2 Então   
        elif ev_re[1].get_tipoEvento() == 2:
            #{
            #Dt_atend <-- amostra a funcao que gera o tempo de atendimento desse 
            Dt_atend = TempoDeAtendimentoCaixa(vetorTDAC[ev_re[1].get_caixaid()]/3600, tma)
            
            #Gera um <Evento3> para <evento> associado ao instante de tempo <clock>+<Dt_atend>
            ev_re[1].set_tipoEvento(3)
            ev_re[1].set_timeEvento(ev_re[1].get_timeEvento(2)+Dt_atend, 3)
            
            #Insere <evento> na fila de eventos <FE>
            FE.insereFilaEventos((ev_re[1].get_timeEvento(3), ev_re[1]))
            #}
        #Senão # <Evento 3>
        elif ev_re[1].get_tipoEvento() == 3:
            #{
            #Coloca <evento> na lista de saida de clientes <saida> # <Classe ListaSaidaCientes>
            saida.insereListaSaida(ev_re[1])
            
            #O caixa identificado como <caixaid> associado a <evento> é sinalizado como livre
            sinalCaixaLivre[ev_re[1].get_caixaid()] = True
            
            #Se existem clientes nessa fila Então
            if vetorFilaCaixa[ev_re[1].get_caixaid()].FilaCaixaEstaVazia() is False:
            #{
                #<proximoevento> <-- retira evento da fila do caixa
                cliente_ev2 = vetorFilaCaixa[ev_re[1].get_caixaid()].retiraFilaCaixa()
                
                #Loga o estado das filas em <logfilas>
                temp = (nCaixas+1)*[None]
                temp[0] = ev_re[1].get_timeEvento(3)
                for i in range(nCaixas):
                    temp[i+1] = TamanhoDasFilas(vetorFilaCaixa[i])
                logfilas.append(temp)
                
                #atualiza o gráfico
                grafico_temp.append(temp)
                #Cria um <Evento2> aassociado a <proximovento> associado ao instante de tempo <clock>
                cliente_ev2.set_tipoEvento(2)
                cliente_ev2.set_timeEvento(ev_re[1].get_timeEvento(3), 2)
                FE.insereFilaEventos((ev_re[1].get_timeEvento(3), cliente_ev2))
                #Insere <proximoevento> na fila de ventos <FE>
                
                sinalCaixaLivre[cliente_ev2.get_caixaid()] = False
                #}
            #}
        #}
    # retorna o gráfico dessa simulação
    return grafico_temp
                
# Programa main
if __name__ == "__main__":
    # taxa de chegada de clientes por hora
    # A simulacao usa segundos mas a taxa por hora é demais
    # facil compreeensao para o usuario
    lambdacliente_hour = 50
   
    # Duracao total do expediente em horas
    duracaoexpediente_hour = 6

    # Definicao dos caixas 
    # mudar nCaixas e vetorTDAC se for mudar quantidade de caixas
    nCaixas=3
    vetorFilaCaixa = nCaixas*[None]
    for k in range(0,nCaixas):
        vetorFilaCaixa[k]=FilaCaixa()

    # taxa de atendimento de cada caixa por hora
    vetorTDAC=nCaixas*[None]
    vetorTDAC[0] = 15
    vetorTDAC[1] = 15
    vetorTDAC[2] = 15
   
    # caixaid = 0,1,2
    tma = 120
    sinalCaixaLivre = nCaixas*[True]

    FE = FilaEventos()
    # lista de clientes aonde sao colocados os objetos da classe
    
    # está na função, é chamada 'todos_os_clientes'
    
    # Cliente quando e' terminado o atendimento 
    saida = ListaClientesSaida()
   
    # lista para monitoracao das filas
    # No inicio [[0,0,0,0]] tempo=0 e tamanho das filas = 0
    # A cada operacao de inercao de cliente na fila ou remocao
    # o estado de todas as filas e' checado 
    # formando uma sub-lista [clock, tam fila1, tam fila 2, tam fila 3]
    # sub-lista e' acrescentada na lista 
    logfilas = []
    numeroderepeticoes = 50
    
    # array para calculo das estatisticas
    listasaida = []
    
    # variável para plotagem de gráfico
    grafico = numeroderepeticoes*[None]
    
    for i in range(numeroderepeticoes):
        #em 'simulacao()' o valor nulo de logfilas não é incluído
        logfilas.append([0]+nCaixas*[0])
        #printa iteração atual
        print("Simulação:", i)
        #recebe o gráfico da simulação atual, para plotar
        grafico[i] = simulacao()
        #enquanto ainda houverem valores na lista de saida
        while saida.ListaSaidaVazia() is False:
            #temp é array para armazenar diferenças de tempo, atualizado no final de cada simulacao
            #fiz dessa forma pois AleatorioAlunos não importa FilasAlunos
            cliente_saida = saida.retiraListaSaida()
            temp = 3*[None]
            temp[0] = cliente_saida.get_timeEvento(2) - cliente_saida.get_timeEvento(1)
            temp[1] = cliente_saida.get_timeEvento(3) - cliente_saida.get_timeEvento(2)
            temp[2] = cliente_saida.get_timeEvento(3) - cliente_saida.get_timeEvento(1)
            #listasaida é uma lista de listas com os valores de temp para calcular estatisticas
            listasaida.append(temp)
            
            
    # Calculo das estatisticas, Medias, Desvios Padroes
    # Media, variancia, tempo na fila, tempo no atendimento e tempo total
    t_fila, t_atend, t_total, v_fila, v_atend, v_total, nm = calculaEstatisticas(listasaida, logfilas)
    
    print("Média da distribuição da chegada de clientes:", lambdacliente_hour/3600)
    print("Variância da distribuição da chegada de clientes:", (lambdacliente_hour/3600)**2)
    print("Média de tempo nas filas:", t_fila)
    print("Variância do tempo nas filas:", v_fila)
    print("Média de tempo nos caixas:",t_atend)
    print("Variância do tempo nos caixas:", v_atend)
    print("Média de tempo total:",t_total)
    print("Variância do tempo total:", v_total)
    print("Número médio de clientes na fila:", nm, ", nCaixas:", nCaixas)
    
    # Plot do estado das filas ao longo do tempo
    # numero de subplots e' dependente de nCaixas
    # cada subplot e'incorporado sequencialmente
    # x = tempo da simulacao em segundos
    # y = tamanho de uma das filas
    # 
    fig, ax = plt.subplots(nCaixas)
    fig.suptitle('Evolucao do Tamanho da Fila')
    nlines = len(grafico[n_simulacao])
    # x recebe a coluna 0 da lista
    x = [row[0] for row in grafico[n_simulacao]]   
    for k in range(1,nCaixas+1):
        # y recebe a coluna k da lista
        y = [row[k] for row in grafico[n_simulacao]]
        ax[k-1].step(x, y)
        ax[k-1].set_xlabel('tempo (s)')
        ax[k-1].set_ylabel('Fila'+str(k-1))
        ax[k-1].grid()
    fig.canvas.draw()


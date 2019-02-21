import read_data as r
import selection as s
import crossover as c
import mutation as mu
import os
import sys
import random
import math as m
import matplotlib.pyplot as plt
import time

def generate_population(p,dic_city):
    population={}
    
    for i in range(0,p):
        population[i]=[random.sample(list(dic_city.keys()), len(dic_city))]
        #puntuacion camino
        population[i].append(score_population(population[i][0],dic_city))
        #fitnes
        population[i].append(0)
    return population

def replace_population(population,dic_city,pos):
    
    for i in range(0, int(len(pos)/2)):
        population[pos[i]]=[random.sample(list(dic_city.keys()), len(dic_city))]
        #puntuacion camino
        population[pos[i]].append(score_population(population[pos[i]][0],dic_city))
        #fitnes
        population[pos[i]].append(1/population[pos[i]][1])
        pos.pop(i)

    return population,pos

def score_population(population,dic):
    score=0
    for i in range(0,len(population)-1):
        d1_q1=abs(dic[population[i]][0]-dic[population[i+1]][0])
        d2_q2=abs(dic[population[i]][1]-dic[population[i+1]][1])
        score+=m.sqrt(m.pow(d1_q1,2)+m.pow(d2_q2,2))

    d1_q1=abs(dic[population[-1]][0]-dic[population[0]][0])
    d2_q2=abs(dic[population[-1]][1]-dic[population[0]][1])
    score+=m.sqrt(m.pow(d1_q1,2)+m.pow(d2_q2,2))
    
    return score

def fitness(x):
    for i in range(0,len(x)):
        population[i][2]=1/population[i][1]
    return population

if __name__ == '__main__':
    # lectura de dataset
    dic_city=r.read_data(sys.argv[1])
    x=[v[0] for k,v in dic_city.items()]
    y=[v[1] for k,v in dic_city.items()]
    
    ini=time.time()
    #plot city
    plt.ion()
    plt.plot(x, y, 'ro')
    plt.axis([min(x), max(x), min(y), max(y)])
    plt.show()


    ##################################Poblacion Inicial###########################
    n_population=300
    #replace: la mitad de este valor se corresponde a nuevos hijos y a poblacion reemplazda
    #es decir si es valor 10, 5 individuos seran generados como hijos y 5 seran
    # los individuos reemplazados por una poblacion aleatoria
    replace=150
    #genera poblacion con x individuos tener en cuenta que se dejan
    #espacios para los hijos. ESto es porque se quiere mantener una talla
    #fija de la poblacion.
    population=generate_population(n_population-int(replace/2),dic_city)
    pos_vacias=[x for x in range(n_population-int(replace/2), n_population)]
    t_seleccio=''
    #padres a seleccionar en las operaciones de seleccion
    n_parents_sel=10
    t_cruce=''
    prob_mut=0.9
    t_mutacion=''
    #############################################################################


    #comprobar fitness inicial
    population=fitness(population)
    
    #generacion actual
    gen=1
    #elegir al mejor individuo de la poblacion
    best=min(population.keys(), key=(lambda k: population[k][1]))
    mejor={}
    mejor[0]=population[best]

    #parámetros mutación, cruce y numero de padres
    mutacion=1

    #tamaño corte para el cruce ordenado. Este parametro se actualiza cada ciertas 
    #generaciones
    cross_over=45

    #Numero de generaciones a realizar
    iters=1000

    
    y_1=list()
    while(gen<iters):
    
        gen+=1
        #actualización de los parámetros del cruce ordenado y
        # de la mutación por intercambio si se emplea.
        if(gen%500==0 and cross_over>5):
            mutacion-=0
            cross_over-=5
        
        #seleccion de padres
        #######################SEleccion Ruleta######################
        #sel_parents,key_parents=s.roulette(population, n_parents_sel,mejor,best)
        #t_seleccio='rueda ruleta'
        ########################Seleccion Grupos#####################
        sel_parents,key_parents=s.deterministic(population,mejor,n_parents_sel)
        t_seleccio='torneo'
        n_parents=len(sel_parents)
       

        ####################CRUCES#######################################
        """
        Aquí han quedado lugares en la población desierto en la operacion
        de reemplazo y seran los que ocuparan los hijos. En el reemplazo
        se ha guardado al mejor padre y el resto tienen la probabilidad de 
        ser reemplazados. Pos_vacias son los huecos de la población
        que se deben de ocupar.

        Para utilizar unos de los cruces implementados, hay que descomentar
        el cruce que se quiera utilizar y comentar los otros dos.
        """
        #############ORDER CROSSOVER####################################
        #for i in pos_vacias:#este va
        #    population=c.order_crossover(population,cross_over,i,n_parents,sel_parents)
        #t_cruce='Ordenado'
        #################################################################
        
        ##################Cycle CROSSOVER V2#############################
        for i in pos_vacias:
            population=c.cycle_crossover_1(population,n_parents,i,sel_parents)
        #t_cruce='Ciclo'
        ################################################################

        ##################PAIR CROSSOVER ###############################
        #pasar tamaño de corte (population,n_parents,corte,key)
        #for i in pos_vacias:
        #    population=c.crossover_pairs(population,n_parents,2,i,sel_parents)
        #t_cruce='Parejas'
        ################################################################
        


        ###################MUTACIONES###################################
        """
            Aquúi se realizan las operaciones de mutación. Se ha descomentar
            la que se quiere utilizar y comentar las otras dos. La probabilidad
            de mutación se ha definidio anteriormente
        """
        #population=mu.mutation_position(population,mutacion,n_parents,prob_mut,key_parents)
        #t_mutacion='intercambio'
        #population=mu.mutation_intersec(population,n_parents,prob_mut,key_parents)
        #t_mutacion='interseccion'
        population=mu.reverse_seq(population,key_parents,prob_mut)
        t_mutacion='inverso'
        
        #Calcualar distancia para la población mutada
        for i in range(0,len(population)):
            population[i][1]=score_population(population[i][0],dic_city)
        
        #calcular fitnes
        population=fitness(population)
        
        #guardamos al mejor individuo
        best=min(population.keys(), key=(lambda k: population[k][1]))

        ###################REEMPLAZO###################################
        """Remplazamos cierta parte de la población. Aseguramos que
           no quitamos al mejor individuo.
           seleccionamos un numero de individuos aleatorio"""

        pos_vacias=list()
        while(len(pos_vacias)!=int(replace/2)):
            #print('aqui')
            a=random.randint(1,len(population)-1)
            #print(a,pos_vacias, best)
            if a not in pos_vacias and a != best:
                pos_vacias.append(a)
                del population[a]
        
        #De los individuos eliminados vamos a generar la mitad de poblacion
        #aleatoria y dejar lugares de la población para que se creen  hijos
        population,pos_vacias=replace_population(population,dic_city,pos_vacias)
        
        ###############################################################
        best=min(population.keys(), key=(lambda k: population[k][1]))
        mejor[0]=population[best]
        y_1.append(mejor[0][1])

        #if(gen%1==0):
        #    print("----------------Generacion",gen,mutacion,"------------------------------")
        #    print(mejor[0][1])
    
    tiempo=time.time()-ini
    print("Fitness Mejor individuo-> ",mejor[0][1])
    print("Tiempo en segundos: ",tiempo)
    for i, j in zip(population[best][0], population[best][0][1:]):
            plt.plot([x[i-1],x[j-1]], [y[i-1],y[j-1]], 'ro-')
            plt.draw()
            plt.pause(0.001)

    p1=population[best][0][0]-1
    p2=population[best][0][-1]-1
    plt.plot([x[p1],x[p2]], [y[p1],y[p2]], 'ro-')
    plt.draw()
    
    input()
    #print("Población=",str(n_population),", Reemplazo=",str(replace),", Tipo Selec=",t_seleccio,", Nº padres",str(n_parents_sel),", Tipo cruce=",t_cruce, ", Tipo muta=",t_mutacion, ", Mejor resultado=", str(y_1[-1]))
    plt.gcf().clear()
    x_1=[x for x in range(1,iters)]

    plt.plot(x_1, y_1, 'o-')
    """plt.text(0, iters+50, u'Población', fontsize = 10, horizontalalignment='center', verticalalignment='center')
    plt.text(0, iters+40, u'Reemplazo', fontsize = 10, horizontalalignment='center', verticalalignment='center')
    plt.text(0, iters+30, u'Selección', fontsize = 10, horizontalalignment='center', verticalalignment='center')
    plt.text(0, iters+20, u'Cruce', fontsize = 10, horizontalalignment='center', verticalalignment='center')
    plt.text(0, iters+10, u'Mutación', fontsize = 10, horizontalalignment='center', verticalalignment='center')
    plt.text(y_1[-1]-100, iters+50, u'Solución encontrada=', fontsize = 10, horizontalalignment='center', verticalalignment='center')"""
    plt.draw()
    input()
    plt.gcf().clear()

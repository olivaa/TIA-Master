import read_data as r
import crossover as c
import mutation as mu
import os
import sys
import random
import math as m
import matplotlib.pyplot as plt
import time

"""
Función encargada de generar la población inicial
"""
def generate_population(p,dic_city):
    population={}
    
    for i in range(0,p):
        population[i]=[random.sample(list(dic_city.keys()), len(dic_city))]
        #puntuacion camino
        population[i].append(score_population(population[i][0],dic_city))
        #fitnes
        population[i].append(0)
    return population

"""
Función para calcular distancia, en este caso el fitness
"""
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

if __name__ == '__main__':
    # lectura de dataset
    dic_city=r.read_data(sys.argv[1])
    x=[v[0] for k,v in dic_city.items()]
    y=[v[1] for k,v in dic_city.items()]
    
    
   
    ##################################Poblacion Inicial###########################
    s_inicial=generate_population(1,dic_city)
    s_mejor={}
    s_mejor[0]=[s_inicial[0][0],10e20,0]
    #############################################################################

    iters=1
    y_1=list()
    x_mejores=list()
    y_mejores=list()
    aleatorio=generate_population(1,dic_city)
    ini=time.time()
    for i in range(0,1):
        #Aquí se establecen los parámetros principales del algoritmo
        t_inicial=10e10
        t_final=1e-30
        enfriamiento=0.995

        #generar una solución aleatoria para el primer cruce
        aleatorio=generate_population(1,dic_city)
        #tamaño bloque para el cruce ordenado. Actualizar parametro
        cro=45
        while(t_inicial>t_final):
            iters+=1
            s_nueva={}
            
            ######################Perturbar Solución##########################
            s_nueva[0]=[s_inicial[0][0],0,0] #Important per a no modificar al vell


            #############ORDER CROSSOVER####################################
            #Actualización del prametro referente al tamaño de bloque
            if(iters%1000==0 and cro>0):
                cro-=3

            #Generación de una solución vecina a partir del cruce
            if aleatorio != s_inicial:
                s_nueva[0][0]=c.order_crossover(s_inicial,aleatorio,cro)
            else:
                aleatorio_2=generate_population(1,dic_city)
                s_nueva[0][0]=c.order_crossover(s_inicial,aleatorio_2,12)
            
        
            #####################MUTACION###########################
            #s_nueva=mu.mutation_position(s_nueva,1)
            s_nueva=mu.reverse_seq(s_nueva)
            
            #calcular dist vecindario
            s_nueva[0][1]=score_population(s_nueva[0][0],dic_city)
            
            
            diferencia= s_nueva[0][1]-s_inicial[0][1]
            if diferencia<0 or m.exp(-diferencia/t_inicial)>random.uniform(0,1):
                if diferencia<0: 
                    aleatorio[0][0]=s_nueva[0][0]
                
                if s_nueva[0][1] < s_mejor[0][1]:
                    s_mejor[0][0]=s_nueva[0][0]
                    s_mejor[0][1]=s_nueva[0][1]
                    s_mejor[0][2]=s_nueva[0][2]
                    y_mejores.append(s_mejor[0][1])
                    x_mejores.append(iters)


                s_inicial[0][0]=s_nueva[0][0]
                s_inicial[0][1]=s_nueva[0][1]
                s_inicial[0][2]=s_nueva[0][2]
            
            y_1.append(s_inicial[0][1])
            t_inicial=t_inicial*enfriamiento

            #print("----------------Generacion",t_inicial,"------------------------------")
            #print(s_inicial[0][1])
    
    print("Mejor solución encontrada->",s_mejor[0][1])
    tiempo=time.time()-ini
    print("Segundos",tiempo)

    for i, j in zip(s_mejor[0][0], s_mejor[0][0][1:]):
            plt.plot([x[i-1],x[j-1]], [y[i-1],y[j-1]], 'ro-')
            plt.draw()
            plt.pause(0.001)

    p1=s_inicial[0][0][0]-1
    p2=s_inicial[0][0][-1]-1
    plt.plot([x[p1],x[p2]], [y[p1],y[p2]], 'ro-')
    plt.draw()
    
    
    input()
    plt.gcf().clear()
    x_1=[x for x in range(1,iters)]
    plt.plot(x_1, y_1, 'o-',markersize=1)
    plt.plot(x_mejores,y_mejores, 'o-',markersize=1)
    plt.draw()
    input()
    plt.gcf().clear()

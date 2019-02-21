import os
import sys
import math
import random

"""
best indica si se queda con el mejor padre
"""
def roulette(population,parents,best,k_p):
    sel_parents={}
    roulette=[]
    #prob_parents=[0]*len(population)
    
    #calcular el sumatorio de fitnes de los individuos
    sum_fit=[population[key][2] for key in population.keys()]
    sum_fit=sum(sum_fit)
    l=[k for k,v in population.items()]
    #calcular la prob de cada uno de los individuos segun el valor de su fitnes
    #crear la ruleta
    for i in l:
        prob_parents=(round(population[i][2]/sum_fit,2))
        n=int(prob_parents*100)
        p=[i]*n
        roulette.extend(p)
    #seleccionar dos individuos al azar de la ruleta(
    key_parents=list()
    for i in range(0,parents):
        k_parent=roulette[random.randint(0,len(roulette)-1)]
        sel_parents[i]=population[k_parent]
        key_parents.append(k_parent)

    #Si no se ha elegido al mejor padre de la generación anterior, lo añadimos
    #a la lista de padres
    diffkeys = [k for k in sel_parents if sel_parents[k] == best[0]]
    if(len(diffkeys)==0):
        sel_parents[parents]=best[0]
        key_parents.append(k_p)
    #key_parents=[k for k,v in sel_parents.items()]
    return sel_parents,key_parents

def deterministic(population,best,n_groups):
    sel_parents={}
    #calculo miembros de un grupo
    members=round(len(population)/n_groups)
    #creamos los grupos de forma aleatoria
    numbers=random.sample(list(population.keys()), len(population))
    #lista para almacenar los grupos
    groups=[[]]*n_groups
    ini=0
    for i in range(0,n_groups-1):
        groups[i]=numbers[ini:ini+members]
        ini+=members
    groups[n_groups-1]=numbers[ini:]
    
    #seleccionamos al mejor de cada grupo. A diferencia de la ruleta aquí se asegura que
    #siempre nos quedamos con el mejor padre de la generación
    index=0
    #print(population)
    key_parents=list()
    for i in groups:
        score=-9e100
        for j in i:
            if(population[j][2]>score):
                sel_parents[index]=population[j]
                score=population[j][2]
                key_parent=j
        key_parents.append(key_parent)  
        index+=1
    
    return sel_parents,key_parents

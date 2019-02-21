import sys
import os
import random


def order_crossover(s_in,aleatorio,s=5):
    #seleccionar por donde cortar el individuo
    select=random.randint(0,int(len(s_in[0][0])/2))
    
   
    #generar hijo y añadir cromosoma padre1
    child=['a']*len(s_in[0][0])
    child[select:select+s]=s_in[0][0][select:select+s]

    #completar hijo con cromosoma de padre2
    pos=select+s
    for i in range(select+s,len(child)):
        if pos==len(child):
            pos=0
        if aleatorio[0][0][i] not in child:
            child[pos]=aleatorio[0][0][i]
            pos+=1
    for i in range(0,select+s):
        if pos==len(child):
            pos=0
        if aleatorio[0][0][i] not in child:
            child[pos]=aleatorio[0][0][i]
            pos+=1


    return child


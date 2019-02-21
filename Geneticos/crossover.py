import sys
import os
import random

def order_crossover(population,s,n,n_parents,sel_parents):
    #seleccionar por donde cortar el individuo
    select=random.randint(0,int(len(population[0][0])/2))
    
    #seleccionar dos padres
    parents=random.sample(range(n_parents), 2)
    #generar hijo y añadir cromosoma padre1
    child=['a']*len(population[0][0])
    child[select:select+s]=sel_parents[parents[0]][0][select:select+s]

    #completar hijo con cromosoma de padre2
    pos=select+s
    for i in range(select+s,len(child)):
        if pos==len(child):
            pos=0
        if sel_parents[parents[1]][0][i] not in child:
            child[pos]=sel_parents[parents[1]][0][i]
            pos+=1
    for i in range(0,select+s):
        if pos==len(child):
            pos=0
        if sel_parents[parents[1]][0][i] not in child:
            child[pos]=sel_parents[parents[1]][0][i]
            pos+=1
    #nuevo hijo
    population[n]=[child]
    #distancia hijo
    population[n].append(0)
    #fitness hijo
    population[n].append(0)

    return population

def cycle_crossover_1(population,n_parents,n,sel_parents):#REVISAR
    k_p=[k for k,v in sel_parents.items()]
    parents=random.sample(k_p, 2)
    child=['a']*len(population[0][0])
    i=0
    while(sel_parents[parents[0]][0][i] not in child):
        child[i]=sel_parents[parents[0]][0][i]
        i=sel_parents[parents[1]][0][i]-1

    i=0
    for i in sel_parents[parents[1]][0]:
        if i not in child:
            child[child.index('a')]=i

    #nuevo hijo
    population[n]=[child]
    #distancia hijo
    population[n].append(0)
    #fitness hijo
    population[n].append(0)

    

    return population

def crossover_pairs(population,n_parents,n_cut,n,sel_parents):

    k_p=[k for k,v in sel_parents.items()]
    parents=random.sample(k_p, 2)
    child=['a']*len(population[0][0])
    i=0
    pos=0

    for j in range(0,int(len(population[0][0])/n_cut)):
        if(len(list(set(sel_parents[parents[0]][0][pos:pos+n_cut]) & set(child)))==0):
            child[i:i+n_cut]=sel_parents[parents[0]][0][pos:pos+n_cut]
            i+=2
        if(len(list(set(sel_parents[parents[1]][0][pos:pos+n_cut]) & set(child)))==0):
            child[i:i+n_cut]=sel_parents[parents[1]][0][pos:pos+n_cut]
            i+=2
        pos+=2
    

    for j in range(0,len(population[0][0])):
        if(sel_parents[parents[0]][0][j] not in child):
            child[i]=sel_parents[parents[0]][0][j]
            i+=1
        if(i==len(sel_parents[0][0])):
            break
        if(sel_parents[parents[1]][0][j] not in child):
            child[i]=sel_parents[parents[1]][0][j]
            i+=1
        if(i==len(population[0][0])):
            break

    #nuevo hijo
    population[n]=[child]
    #distancia hijo
    population[n].append(0)
    #fitness hijo
    population[n].append(0)
    return population


def cycle_crossover(population,n_parents,n_child):
    #seleccionar dos padres
    parents=random.sample(range(n_parents), 2)
    
    #generar hijos
    child_1=['a']*len(population[0][0])
    child_2=['a']*len(population[0][0])

    child_1[0]=population[parents[0]][0][0]
    child_2[0]=population[parents[1]][0][0]

    p2_in_c1=True
    i=0
    while(p2_in_c1):
        j=population[parents[0]][0].index(population[parents[1]][0][i])
        print("Valor de I->", i)
        print("Valor de J->",j)
        input()
        print(population[parents[0]][0][j],'en',j,'en',population[parents[1]][0][i])
        print(population[parents[0]])
        print(population[parents[1]])
        input()
        print(parents,"PARES")
        child_1[j]=population[parents[0]][0][j]
        child_2[j]=population[parents[1]][0][j]
        i=j
        print(population[parents[1]][0][i],'en',child_1)
        print(population[parents[1]][0][i] not in child_1)
        if(population[parents[1]][0][i] not in child_1):
            p2_in_c1=False
   
    
    for i in range(0,len(child_1)):
        if(child_1[i]=='a'):
            child_1[i]=population[parents[1]][0][i]
            child_2[i]=population[parents[0]][0][i]
    
    #nuevo hijo
    population[n_child]=[child_1]
    #distancia hijo
    population[n_child].append(0)
    #fitness hijo
    population[n_child].append(0)
    #nuevo hijo
    population[n_child+1]=[child_2]
    #distancia hijo
    population[n_child+1].append(0)
    #fitness hijo
    population[n_child+1].append(0)
    print(population)
    return population

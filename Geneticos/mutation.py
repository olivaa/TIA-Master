import random
import sys
import os

def mutation_position(population,n_cromo,n_parents,prob,key_parents):
    
    p=random.randint(1,100)
    numbers=[x for x in range(0,len(population[0][0]))]
    for i in range(0,len(population)):
        if(i not in key_parents):
            if(p>=prob):
                n1=random.sample(list(numbers), n_cromo)
                n2=random.sample(list(numbers), n_cromo)
                for j in range(0,n_cromo):
                    aux=population[i][0][n1[j]]
                    population[i][0][n1[j]]=population[i][0][n2[j]]
                    population[i][0][n2[j]]=aux
    return population

def mutation_intersec(population,n_parents,prob,key_parents):

    p=random.randint(1,100)
    
    for i in range(0,len(population)):
        if(i not in key_parents):
            if(p>=prob):
                pos=random.randint(0,len(population[0][0])-1) #pos a intercambiar
                val=random.randint(0,len(population[0][0])-1) #indice de valor
                aux=population[i][0][val]
                if pos<val:
                    for j in range(val,pos,-1):
                        population[i][0][j]=population[i][0][j-1]
                    population[i][0][pos]=aux
                elif pos>val:
                    for j in range(val, pos):
                        population[i][0][j]=population[i][0][j+1]
                    population[i][0][pos]=aux
    return population

def reverse_seq(population,key_parents,prob):
    p=random.randint(1,100)
    for i in range(0,len(population)):
        if(i not in key_parents):
            if(p>=prob):
                pos_1=random.randint(0,len(population[0][0])-1) #pos a intercambiar
                pos_2=-1
                while(pos_2<pos_1):
                    pos_2=random.randint(0,len(population[0][0])-1) #indice de valor
                population[i][0][pos_1:pos_2+1]=reversed(population[i][0][pos_1:pos_2+1])
               
    return population
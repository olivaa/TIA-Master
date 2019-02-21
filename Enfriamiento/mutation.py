import random
import sys
import os

def reverse_seq(population):
    
    pos_1=random.randint(0,len(population[0][0])-1) #pos a intercambiar
    pos_2=-1
    while(pos_2<pos_1):
        pos_2=random.randint(0,len(population[0][0])-1) #indice de valor
    population[0][0][pos_1:pos_2+1]=reversed(population[0][0][pos_1:pos_2+1])
    population[0][1]=0
    population[0][2]=0
    return population

import os
import sys

def read_data(filename):
    dic_city={}
    with open(filename) as f:
        lineas=f.readlines()
        for i in range(1,len(lineas)-1):
            if lineas[i].rstrip() == 'EOF': 
                break
            city=lineas[i].split(' ')
            try:
                val = int(city[0])
                dic_city[int(city[0])]=(float(city[1]),float(city[2].split('\n')[0]))
            except:
                print("")
    
    return dic_city
"""
def read_data(filename):
    dic_city={}
    with open(filename) as f:
        lineas=f.readlines()
        for i in range(8,len(lineas)-1):
            if lineas[i].rstrip() == 'EOF': 
                break
            print(lineas[i])
            city=lineas[i].split(' ')
            city=[x for x in city if x!='']
            print(city)
            
            dic_city[int(city[0])]=(float(city[1]),float(city[2].split('\n')[0]))
    
    return dic_city"""

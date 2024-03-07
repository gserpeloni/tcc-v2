import numpy as np
import pandas as pd

def calculoErro (dados, name):
    #Variaveis   
    (d1,d2) = (np.array(dados[0]),np.array(dados[1]) )
    somatorio_dx, somatorio_dy = (0,0)

    #Calculo para o erro quadratico medio (y-y')^2:
    for i in range(len(d1)):
        somatorio_dx += (d1[i]*d1[i])
        somatorio_dy += (d2[i]*d2[i])
    
    #Calculando a Raiz do erro médio ao quadrado
    reqm_x = (somatorio_dx/len(d1)) ** (1/2)   
    reqm_y = (somatorio_dy/len(d2)) ** (1/2)
    
    #Calculando o Vies()
    (vies_1, vies_2) = calculoVies(d1,d2)
      
    df1 = pd.DataFrame({'Somatorio-x': [somatorio_dx], 'Qtd.Dados-x': [len(d1)],'REQM_Dx': [reqm_x], 'Vies_Dx': [vies_1],'   ':'    '})
    df2 = pd.DataFrame({'Somatorio-y': [somatorio_dy], 'Qtd.Dados-y': [len(d2)],'REQM_Dy': [reqm_y], 'Vies_Dy': [vies_2]})
    df3 = pd.concat([df1,df2],axis=1)
    df3.name = name
    
    
    print(df3.name)
    display(df3)

def calculoVies(dx, dy):
    #Variaveis:
    (s_dx,s_dy) = (0,0)
    
    for i in range(len(dx)):
        s_dx += (dx[i])
        s_dy += (dy[i])
        
    vies_1 = (1/len(dx))*s_dx 
    vies_2 = (1/len(dy))*s_dy
        
    return vies_1, vies_2
    
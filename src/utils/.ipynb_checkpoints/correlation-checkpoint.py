import numpy as np
import pandas as pd
import dataFrames as df

def filterWrongTiePoints(dados, limiar, numberRows, name, operatorName):
  #Variaveis   
    dados_filtrados = []
    (dx,dy) = (dados[4], dados[5]) # dx[4] e dy[5]
    matriz = np.zeros((len(dx),2))  
    
    max_valor_dx = np.median(dx)
    max_valor_dx = (max_valor_dx*limiar)+max_valor_dx
    
    max_valor_dy =  np.median(dy)
    max_valor_dy = (max_valor_dy*limiar)+max_valor_dy
    
    
  #Gerando Matriz -- Guarda todos os valores de dx e dy na matriz 0: dx 1: dy
    for i in range(len(dx)):
        matriz[i][0] = dx[i]
        matriz[i][1] = dy[i]
        
  #Maximo e Minimo para filtro dos dados: 
    (f1,f2, descartados) = ([],[],[])
    (m_l, m_c) = matriz.shape
   
 #Calculo para  gerar tiepoints sem erros: 
    for i in range(m_l):    
        if( (matriz[i][0] >= (-1*max_valor_dx) and matriz[i][0] <= max_valor_dx) or 
            (matriz[i][1] >= (-1*max_valor_dy) and matriz[i][1] <= max_valor_dy) ): #entre o valor
            f1.append(matriz[i][0])
            f2.append(matriz[i][1])
        elif( matriz[i][0] > max_valor_dx or matriz[i][0] < (-1*max_valor_dx)  or
            (matriz[i][1] > max_valor_dy or matriz[i][1] < (-1*max_valor_dy)) ): #entre o valor
            descartados.append(i)
        
                
   #Gerando DataFrame     
    dataframe = pd.DataFrame({'Filtro(X)':f1, 'Filtro(Y)': f2})    
    dataframe.name = name
  
   #Lista dos dados filtrados
    dados_filtrados.append(f1) 
    dados_filtrados.append(f2)
    dados_filtrados.append(descartados)
     
        
    #Printando saidas
    print(dataframe.name,"\n - Indices Descartados: ",dados_filtrados[2])
    display(dataframe.head(numberRows))
   
    csvName= "Cordenadas_Filtradas_"+ operatorName + "_" +name
    df.exportarCSV(dataframe,csvName,operatorName)
    return (dados_filtrados)
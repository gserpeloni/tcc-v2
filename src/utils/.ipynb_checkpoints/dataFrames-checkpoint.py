import pandas as pd
import numpy as np

def exportarCSV(dataFrame,nome, operatorName):      
    file = "../tcc/resultados/"+operatorName+'/'+nome+".csv"
    dataFrame.to_csv(file, encoding='utf-8') 
    
def createDataFrame(data1, data2, operatorName):
    #sift_data_x:  {[0]: Keypoints, [1]: Descritores dos Kp, [2]: Imagem com pontos selecionados} 
    (kp_data1,kp_data2) = createDataList(data1, data2)  
    
    d = { 
            'Keypoints Img1': [ len(kp_data1[0]) ], 
            #'Descritores Img1':[ len(kp_data1[1]) ],
            'Keypoints Img 2': [ len(kp_data2[0]) ],
            #'Descritores Img2':[ len(kp_data2[1]) ] 
     }

    data = pd.DataFrame(d) 
    display(data.head())
    
    csvName = "Qtd_Dados_Detectados_"+operatorName+"_"
    exportarCSV(data,csvName, operatorName)
    
def createDataList(data1, data2):
    # Exibir a quantidade de keypoints detectados e descritores detectados: :
    (kp_data1, kp_data2) = ([],[])    
    kp_data1.append(data1[0]), kp_data1.append(data1[1])
    kp_data2.append(data2[0]), kp_data2.append(data2[1])   
    
    return kp_data1, kp_data2

def getTiePointsSpacialPosition(listKp1, listKp2, numberRows, operatorName, titulo):
   #Variaveis de uso geral: 
    (xv,xv2,yv,yv2,deltax, deltay, dados)  = ([],[],[],[],[],[],[])
    (dX,dY) = (np,np) 

   #Gerando Cordenadas Espaciais Img1: 
    for i in range (len(listKp1)) :
        x, y = listKp1[i]
        xv.append(round(x,5))
        yv.append(round(y,5))

   #Gerando Cordenadas Espaciais Img2:       
    for i in range (len(listKp2)) :
        x2, y2 = listKp2[i]
        xv2.append(round(x2,5))
        yv2.append(round(y2,5))    

        
   #Gerando diferenca entre as cordenadas espaciais: 
    for i in range (len(xv)):    
        dX = xv[i] - xv2[i]
        dY = yv[i] - yv2[i]
        deltax.append(round(dX,5))
        deltay.append(round(dY,5))


    #Transformando a lista em Array:     
    df = pd.DataFrame({'Img1 (X)': xv, 'Img1 (Y)': yv, 'Img2 (X)': xv2, 'Img2 (Y)': yv2, 'deltaX': deltax, 'deltaY': deltay})
#     df = pd.DataFrame({'deltaX': deltax, 'deltaY': deltay})
    
    #Gerando list de dados gerados.
    dados.append(xv), dados.append(yv), dados.append(xv2), dados.append(yv2), dados.append(deltax), dados.append(deltay), dados.append(df)
    
    display("Cordenadas_Espaciais - "+ operatorName)
    display(dados[6].head(numberRows))  
    
    if(titulo != ""): 
        exportarCSV(df,"Cordenadas_Espaciais_"+ operatorName + titulo, operatorName)
    
    return dados
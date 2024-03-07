'''
@author: Gustavo Serpeloni
@description: Funçoes para conversao do sistema de imagem para o sistema fotogametrico 
(Câmeras Digitais)
@date: 24.04.2020
@version: 1.0
'''

#-------------    Importações   --------------------
import math
import pandas as pd

#TRASNFORMCAO PAR AO CENTRO DA IMAGEM [COORDENADA DOS KEYPOINTS -> MM em relacao ao cnetro]
def transformacao (tie, tamPixels, cx, cy): 
    data = []
    col = len(tie[0])
    lin = len(tie)
    tam_px = float(tamPixels)
    #display(data, col, lin, tam_px)
    
    for i in range(lin):
        for j in range(col-1):
        #-- Trocando os eixos: 
            x =   (tie[i][j] - cx)*tam_px
            y =  -(tie[i][j+1] - cy)*tam_px

     #Caso Necessite rotacionar os dados para 90 graus:
            x_rot = y
            y_rot = -x
            data.append([round(x_rot,5), round(y_rot, 5)])
     
    
    #CRIAR UMA FUNCAO IGUAL PARA AMBAS        
    dataF = []
    for i in range(len(data)):
         dataF.append({'X':  data[i][0], 'Y': data[i][1]})
    
    display(pd.DataFrame(dataF)); 
    return data


def transladar_pontos(data_points, x0, y0):
    data = []
    col = len(data_points[0])
    lin = len(data_points)

    for i in range(lin):
        for j in range(col-1):
            xf= (float(data_points[i][j])) - x0
            yf= (float(data_points[i][j+1])) - y0
            data.append([round(xf,5), round(yf, 5)])
            
    
    #CRIAR UMA FUNCAO IGUAL PARA AMBAS
    dataF = []
    for i in range(len(data)):
         dataF.append({'X':  data[i][0], 'Y': data[i][1]})
    
    #display(pd.DataFrame(dataF)); 
    return data


def correcao_distorcado_radial_simetrica(data_translocada,data_tranform, k1, k2, k3):
    data = []
    col = len(data_translocada[0])
    lin = len(data_translocada)

    for i in range(lin):
        for j in range(col-1):
            xf = float(data_translocada[i][j])
            yf = float(data_translocada[i][j+1])
            x =  float(data_tranform[i][j])
            y=  float(data_tranform[i][j+1])

            r = math.sqrt (xf*xf+yf*yf)
            r2 = r*r
            r4 = r2*r2
            r6 = r4*r2
            
            dx = x*( (float(k1)*r2) + (float(k2)*r4) + (float(k3)*r6) )
            dy = y*( (float(k1)*r2) + (float(k2)*r4) + (float(k3)*r6 ) )
            #dx, dy = (0,0)
            
            xf = xf - dx
            yf = yf - dy
            
            data.append([r, r2, r4, r6, dx, dy, xf, yf]);
            
 
    dataF = []
    for i in range(len(data)):
         dataF.append({
                    #'r':  data[i][0], 
                    #'r2': data[i][1], 
                    #'r4': data[i][2], 
                    #'r6': data[i][3], 
                    #'dx': data[i][4], 
                    #'dy': data[i][5], 
                    'xf': data[i][6],
                    'yf': data[i][7]
         })
            
    display(pd.DataFrame(dataF).head(5)); 
    return data


def dep_RO(data_img1, data_img2,focalLength):
    arquivo = open("dep_ro.dat", 'w')
    data_transladado_img1, data_transladado_img2  = ([], [])
    data_transladado_img1, data_transladado_img2  = (data_img1[1], data_img2[1])
    qtd_pontos = len(data_transladado_img1)

    print("\n\nQuantidade de pontos Dep-RO: ", qtd_pontos, "Focal:", str(focalLength))
    arquivo.write(str(qtd_pontos)+"\n")

    for i in range(qtd_pontos):
        value1 = str(data_transladado_img1[i][0])[:4];
        value2 = str(data_transladado_img1[i][1])[:4];
        value3 = str(data_transladado_img2[i][0])[:4];
        value4 = str(data_transladado_img2[i][1])[:4];
        
        txt =  value1+"\t"+value2+"\t"
        txt += value3+"\t"+value4+"\n"
        arquivo.write(txt)    


    #Parametros do sistema  (By, Bz, omega, phi , kappa) e Parametros Bx e Focal: 
    Bx = float(data_transladado_img1[0][0]) - float(data_transladado_img2[0][0])  # X da esquerda - x dad direita
    txt =  "0.0 0.0 0.0 0.0 0.0" + "\n" + str(Bx) +" "+ str(data_img1[3][3]) + "\n\n"
    arquivo.write(txt)


    print("Valor de Bx:", Bx)
    arquivo.close()
'''
@author: Gustavo Serpeloni
@description: Funçoes para conversao do sistema de imagem para o sistema fotogametrico 
(Câmeras Digitais)
@date: 24.04.2020
@version: 1.0
'''

#-------------    Importações   --------------------
import math

#--------------- Vector Data ----------------------

#sensores: s = [ [nome_sensor, numero_sensor], [col, linha] ,[tam_px],[tam_focal] , [pt_x0, pt_y0] ,[k1, k2, k3], [p1, p2] ]
#- (k1,k2,k3) = Distorcao Radial
#- (p1, p2) = Distorcao Descentrada

#poi_s =  [ [sensor1], [sensor2] ] 

#Tie Points: tie_points = [ [xi,yi], [xi+1, yi+1], ... ,[xn,yn] ]


#- 1. Conversor para sistema fotogametrico 
def convert_sist(img_original):
    poi_s = []
    poi_s = orient_interior()



#- 2. Dados dos parametros de orientacao interior: 
def orient_interior(path_s1, path_s2,path_tie, title):    
    data_POI, data_transform, tie_points, s1,s2 = ([], [], [], [], [])
    
    s1 = leitura_arquivos(path_s1)    
    s2 = leitura_arquivos(path_s2)
    tie = leitura_arquivos(path_tie)


    #Dados do sensor: 
    print("\n0.Dados de Entrada do Sensor:\n",s1)

    #centro de coordenadas do sistema:
    cx = (int(s1[1][0]) - 1 )/2
    cy = (int(s1[1][1]) -1 )/2
    print ("\n2. Centro do Sistema de Imagem:\n","cx:  ", cx, " - cy:   ",cy,"\n")



    # Calculando os tie_points - *separar os tiePoitns (camera Rikola)
    print("3. Tie - Points:\n", tie,"\n")
    data_transform = transformacao(tie, s1, cx, cy)
    write_data(data_transform, title+"_tie_points_transformacao.txt")


    #Translandando Pontos para o centro da imagem
    data_transladada = transladar_pontos(data_transform, s1)
    write_data(data_transladada, title+"_tie_points_transladado.txt")



    #Correcao Radial Simetrica: 
    data_correc = correcao_distorcado_radial_simetrica(data_transladada, data_transform, s1)
    write_correc_distorc(data_correc, title+"_correcao_distorcado_radial_simetrica")

    #Fechando Arquivos:

    #Retornando os dados para criar uma saida de Dep_Ro Global
    return data_transform, data_transladada, data_correc, s1 



def write_data(data, arqName):
    arquivo = open(arqName, 'w')
    col = len(data[0]) 
    lin = len(data)
    
    for i in range(lin):
        for j in range(col-1):
            txt = str(data[i][j]) + "\t" + str(data[i][j+1]) + "\n" #modificar 
            arquivo.write(txt)    
    arquivo.close()
    print("Dados salvos com sucesso !")


#3. Leitura dos dados de entrada de POI ou  TiePoints:
def leitura_arquivos(path):
    cont = 0
    file = open(path)
    data = []
    
    for linha in file:
        line = linha.split()

        if line == [] :
            break

        data.append(line)
        cont = cont + 1
        

    file.close()
    return data



def transformacao (tie, sensor, cx, cy): 
    data = []
    col = len(tie[0])
    lin = len(tie)
    tam_px = float(sensor[2][0])

    for i in range(lin):
        for j in range(col-1):
        #-- Trocando os eixos: 
            x =   (float(tie[i][j].replace(",",".")) - cx)*tam_px
            y =  -(float(tie[i][j+1].replace(",",".")) - cy)*tam_px

     #Caso Necessite rotacionar os dados para 90 graus:
            x_rot = y
            y_rot = -x
            data.append([round(x_rot,5), round(y_rot, 5)])
 

    print ("\n\n4. Dados Calculados:\n",data, "\n\n")
    return data


def transladar_pontos(data_points, sensor):
    data = []
    col = len(data_points[0])
    lin = len(data_points)
    x0 = float(sensor[4][0])
    y0 = float(sensor[4][1])


    for i in range(lin):
        for j in range(col-1):
            xf= (float(data_points[i][j])) - x0
            yf= (float(data_points[i][j+1])) - y0
            data.append([round(xf,5), round(yf, 5)])
            
    print ("\n5. Dados Transladados para o ponto principal:\n",data, "\n\n")
    return data



def correcao_distorcado_radial_simetrica(data_translocada,data_tranform, sensor):
    data = []
    col = len(data_translocada[0])
    lin = len(data_translocada)
    k1, k2, k3 = (sensor[5][:])

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
            data.append([r, r2, r4, r6, dx, dy, xf, yf])
    
    print("\n6. Dados de Correcao da Distorcao Radial Simetrica:\n",data,"\n")
    return data


def write_correc_distorc(data, arqName):
    arquivo = open(arqName, 'w')
    col = len(data[0]) 
    lin = len(data)
    
    arquivo.write(str(lin)+"\n")
    for i in range(lin):
            txt = str(data[i][0])+"\t"+ str(data[i][1])+"\t"+str(data[i][2])+"\t"+ str(data[i][3])
            txt += str(data[i][4])+"\t"+ str(data[i][5])+"\t"+str(data[i][6])+"\t"+ str(data[i][7]) + "\n"
            arquivo.write(txt)    

    arquivo.write("\n\n#Disposicao dos dados:  \nr, r2, r4, r6, dx, dy, xf, yf")
    arquivo.close()
    print("- Correcao de Distorcao radial simetrica Criada !")



# ---------------------------------------------------------------------------------------
''' Funcao para gerar os dados para  entrada doo dep_RO:
    data_img = [[data_transf], [data_transladado], [data_correcao_readiometrica], [SensorX] ]
    [data_transf] = [[x1,y1], [x2,y2], ..., [xn, yn]]
    [data_transladada] = [[x1,y1], [x2,y2], ..., [xn, yn]]

'''
def dep_RO(data_img1, data_img2,focalLength):
    arquivo = open("dep_ro.dat", 'w')
    data_transladado_img1, data_transladado_img2  = ([], [])
    data_transladado_img1, data_transladado_img2  = (data_img1[1], data_img2[1])
    qtd_pontos = len(data_transladado_img1)
    

    print("\n\nQuantidade de pontos Dep-RO: ", qtd_pontos, "Focal:", str(focalLength))
    arquivo.write(str(qtd_pontos)+"\n")

    for i in range(qtd_pontos):
            txt =  data_transladado_img1[i][0]+"\t"+data_transladado_img1[i][1]+"\t"
            txt += data_transladado_img2[i][0]+"\t"+sdata_transladado_img2[i][1]+"\n"
            arquivo.write(txt)    


    #Parametros do sistema  (By, Bz, omega, phi , kappa) e Parametros Bx e Focal: 
    Bx = float(data_transladado_img1[0][0]) - float(data_transladado_img2[0][0])  # X da esquerda - x dad direita
    txt =  "0.0 0.0 0.0 0.0 0.0" + "\n" + str(Bx) +" "+ str(data_img1[3][3]) + "\n\n"
    arquivo.write(txt)


    print("Valor de Bx é:", Bx)


    arquivo.close()

#Rodando as funcoes criadas  - sistema fotogametrico (path_sensor1, path_sensor2, path_tie_points_1, path_tie_points_2):

data_img1 = orient_interior("s1.txt", "s1.txt", "tie_points_img_1_02924.txt", "02924")
data_img2 = orient_interior("s1.txt", "s1.txt", "tie_points_img_2_03000.txt", "03000")

dep_RO(data_img1, data_img2)

print("Dados gerados com sucesso !")
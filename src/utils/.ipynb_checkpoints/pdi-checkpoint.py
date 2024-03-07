'''
@author: Gustavo Serpeloni
@description: Funçoes para processamento de imagens
@date: 18.10.2019
@version: 1.0
'''

#-------------    Importações   --------------------
import cv2 as CV2
import numpy as np



#---------------    Funções   ----------------------

#1. Operador de Sobel para Gx e Gy: 
def sobel(imagem):
    imagens = []
    gx_Sobel = CV2.Sobel(imagem, CV2.CV_64F, 1, 0, ksize= 5)
    gy_Sobel = CV2.Sobel(imagem, CV2.CV_64F, 0, 1, ksize= 5)
    imagens.append(gx_Sobel)    
    imagens.append(gy_Sobel)
    imagens = np.array(imagens)
    return imagens


#2. Gerando a piramide de Imagens: 
def piramideImagens(imagem):
    #Gerando priamides:
    img_nv1 = CV2.pyrDown(imagem);
    img_nv2 = CV2.pyrDown(img_nv1);
    img_nv3 = CV2.pyrDown(img_nv2);

    #Aplicando imagens no Array: 
    imagens = []
    imagens.append(img_nv1)
    imagens.append(img_nv2)
    imagens.append(img_nv3)
    imagens = np.array(imagens)
    return imagens


#3. Gerando imagem Equalizada a partir do Clahe
def claheHistogram(imagem):
    clahe = CV2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
    cl1 = clahe.apply(imagem)
    return cl1
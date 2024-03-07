#-------------    Importações   --------------------
import cv2
import matplotlib.pyplot as plt

def write_Image(nome,img):
    cv2.imwrite('../tcc/'+nome,img)
    
def openImgs(titulo):
    imgs= []  
   
    img1 = cv2.imread('img/entrada/'+'bd01.pgm',0)
    img2 = cv2.imread('img/entrada/'+'bd10.pgm',0)
    imgs.append(img1)
    imgs.append(img2)
    
    #Plotando Imagem de Entrada: 
    img_side_by_side2(imgs, titulo)
    
    return imgs

def img_side_by_side(data,titulo):
    #Configuracoes
    plt.figure(figsize=(15,10))

    #PLotando as imagens:
    configPlot(titulo)
    
    #Imagem 1:
    plt.subplot(1,3,1) # row 0, col 0
    plt.imshow(data[0][2], cmap='gray', vmin=0, vmax=255)
    
    
    #Imagem 2:
    plt.subplot(1,3,2) # row 0, col 1
    plt.imshow(data[1][2], cmap='gray', vmin=0, vmax=255)  

    
def img_side_by_side2(image_datas, titulo):
    #Configuracoes
    plt.figure(figsize=(20,10))

    #PLotando as imagens
    plt.suptitle(titulo, fontsize=15)
    plt.subplots_adjust(top=0.95)   
    plt.subplots_adjust(bottom=0.01)

    plt.subplot(3,3,1) # row 0, col 0
    plt.imshow(image_datas[0], cmap='gray', vmin=0, vmax=255)
    
    plt.subplot(3,3,2) # row 0, col 1
    plt.imshow(image_datas[1], cmap='gray', vmin=0, vmax=255)
    
    #Plotando Histograma 
    plt.subplot(3,3,3) # row 0, col 1
    plt.plot(cv2_histogram(image_datas[0]), "b")
    plt.plot(cv2_histogram(image_datas[1]), "r")
    plt.show()
    
    
def cv2_histogram(img):
   return cv2.calcHist([img], [0], None, [256], [0,256])

def configPlot(titulo):
    plt.suptitle(titulo,x=0.1, y=.95, horizontalalignment='left', verticalalignment='top', fontsize = 12)
    plt.subplots_adjust(top=(1.58))  
    plt.subplots_adjust(bottom=0.012)
    

def salvarImg(nome_img, img_match): 
    write_Image("../tcc/resultados/"+nome_img, img_match)
    
    
def mplot_openImg(img,titulo):
    plt.rcParams['figure.figsize'] = (10,10)
    configPlot(titulo)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()
    
    
def show_vector_Imgs(img):
    for i in range(0, img.shape[0]):
        plt_openImg(img[i])
        
        
def gerarHistograma(img1,img2):
    #Gerando Histograma: 
    plt.rcParams['figure.figsize'] = (30,6)

    histograma_1 = cv2_histogram(img1)
    histograma_2 = cv2_histogram(img2)
    
    plt.plot(histograma_1, "b")
    plt.plot(histograma_2, "r")
    plt.show()
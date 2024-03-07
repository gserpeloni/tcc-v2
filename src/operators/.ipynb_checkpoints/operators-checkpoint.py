import cv2

def SIFT(imagem):
    #Variaveis:    
    data_sift = []
    
    # Instanciondo Operador SIFT: 
    sift = cv2.xfeatures2d.SIFT_create()
    
    #Definindo dados de entrada: 
    gray = imagem
    kp, descr_kp = sift.detectAndCompute(gray,None)
    data_sift.append(kp), data_sift.append(descr_kp)
    
    #Desenhando os keypoints na imagem original:
    img_sift = cv2.drawKeypoints(gray,kp,imagem,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    data_sift.append(img_sift)
            
    return data_sift

def ORB(img1): 
    #variaveis: 
    data_orb = []
 
    #Instanciando operador  
    orb = cv2.ORB_create()
    
    #Coleta Kp e Descritores:
    gray = img1
    
    kp_orb, desc_orb = orb.detectAndCompute(gray,None)    
    data_orb.append(kp_orb), data_orb.append(desc_orb)
  
    img_orb = cv2.drawKeypoints(gray,kp_orb,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    data_orb.append(img_orb)
    
    return data_orb

def SURF(img1): 
    #Variaveis: 
    data_surf = []
 
    #Instanciando operador  
    surf = cv2.xfeatures2d.SIFT_create(100)
    
    #Coleta Kp e Descritores:
    gray = img1    
    
    kp_surf, desc_surf = surf.detectAndCompute(gray,None)    
    data_surf.append(kp_surf), data_surf.append(desc_surf)
  
    img_surf = cv2.drawKeypoints(gray,kp_surf,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    data_surf.append(img_surf)
    
    return data_surf

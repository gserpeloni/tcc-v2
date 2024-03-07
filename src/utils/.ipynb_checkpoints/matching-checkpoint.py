import cv2
import imagesFunctions as img

def matching(data1, data2, kp_selecionados):
    #Descritores:
    
    #Realizando o  matching entre as imagens : 
    img_match = cv2.drawMatchesKnn(data1[2],data1[0],data2[2],data2[0],kp_selecionados,None,
                                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    #Imagem com matching aplicado
    return img_match

def bf_matching(data1, data2,limiar,nome_img,titulo):
    # Instanciando Brute force
    bf = cv2.BFMatcher()
    
    #Descritores:
    matches = bf.knnMatch(data1[1],data2[1],k=2)

    # Aplicando o teste de Proporçao: 
    kp_selecionados = []
    
    #Lista de cordenadas (x,y) - para amba as imagens: 
    (list_kp1, list_kp2) = ([],[])
    
    #Coletando Coordenadas Espaciais :
    for m,n in matches:
        img2_idx = m.trainIdx #cordenadas (x,y) - segunda imagem
        img1_idx = m.queryIdx #cordenadas (x,y) - primeira imagem
        (x1, y1) = data1[0][img1_idx].pt       
        (x2, y2) = data2[0][img2_idx].pt
    
    #Teste de proporção:
        if m.distance < limiar*n.distance:
            kp_selecionados.append([m])
            list_kp1.append((x1, y1))
            list_kp2.append((x2, y2))
            

    #Realizando o  matching entre as imagens : 
    img_match = matching(data1, data2, kp_selecionados)
    
    #Salvar imagem 
    img.salvarImg(nome_img, img_match) 
        
    #Plotando a imagem
    img.mplot_openImg(img_match,titulo)
    
    #Retornando Lista com as coordenadas espaciais
    return (list_kp1, list_kp2, kp_selecionados)

def bf_matching_reamostrada(data_1,data_2,limiar,descartados,titulo):
    # Instanciando Brute force
    bf2 = cv2.BFMatcher()
    
    #Descritores:
    matches = bf2.knnMatch(data_1[1], data_2[1],k=2)

    # Variaveis:  
    kp_selecionados2 = []
    (list_kp1_1, list_kp2_2) = ([],[])
    (img1_idx, img2_idx) = ([],[])    
    cont = 0
    desc = descartados[cont] + 1
    qtd_desc = len(descartados) -1
    print('Qtd-Itens a serem Descartados: ',len(descartados)) 
        
        
    #Coletando Coordenadas Espaciais e :
    
    for m,n in matches:
        (img1_idx, img2_idx)  = (m.queryIdx, m.trainIdx) #cordenadas (x,y) - 1° e 2° imagem
        (x1, y1) = data_1[0][img1_idx].pt       
        (x2, y2) = data_2[0][img2_idx].pt    
        
        #Teste de proporção e removendo os dados errados #!! ERRO !!)        
        if (m.distance < limiar*n.distance) and (m.queryIdx != desc):
            kp_selecionados2.append([m])
            list_kp1_1.append((x1, y1))
            list_kp2_2.append((x2, y2)) 
        elif(m.queryIdx == desc):
            print('Descartado ', 'm.query:',m.queryIdx , '-  desc:',desc, 'valor: ',(x1,y1))
            cont +=1
            if(cont <= qtd_desc):
                desc = descartados[cont]
         
       
    #Realizando o  matching entre as imagens : 
    img_match = matching(data_1, data_2, kp_selecionados2)
           
    #Plotando a imagem
    mplot_openImg(img_match,titulo)
    
    return list_kp1_1, list_kp2_2
import requests
from bs4 import BeautifulSoup
import os
from collections import deque
import string
#find all(tag,class_="")
prefix = '/wiki/'

def liste_liens(page):
    response = requests.get(page)  
    soup = BeautifulSoup(response.content,"html.parser")
    links = []
    for link in soup.find_all('a',href=True):
        currentLink = link.get('href')
        if(currentLink.startswith(prefix) and ":" not in currentLink and not currentLink.startswith(prefix+'User') and "?" not in currentLink and "=" not in currentLink):
                links.append(currentLink[len(prefix):])  
    return links


        
def svg_dico(dico,fichier):
    f = open(fichier,"a+")
    for key,value in dico.items():
        f.write(key+":"+str(value)+"\n")
    f.close()
def chg_dico(fichier):
    try:
        f = open(fichier,"r")
        dico = {}
        for ligne in f:
            l = ligne.split(":")
            dico[l[0]]=l[1].removesuffix("\n")
        return dico
    except FileNotFoundError as e:
        print(e)
        
        
def sauvegarder_wiki():
    dico = parcours()
    svg_dico(dico,"parcours_graph.txt")

def parcours():
    dico = {}
    file_sommets = deque(["Petyr_Baelish"])
    i = 0
    while(len(file_sommets)>0):
        current_link = file_sommets.popleft()
        temp_list = liste_liens("https://iceandfire.fandom.com"+prefix+current_link)
        dico[current_link] = temp_list
        for lien in temp_list:
            if(lien not in dico and lien not in file_sommets):
                file_sommets.append(lien)
        #print(dico)
    return dico           


def plus_court_chemin(source,cible):
    try:
        dico = chg_dico("test_graph.txt")
        parents = {}
        explored = [source]
        stop = False
        while(len(explored)>0 and not stop):
            src = explored.pop(0)
            source_list = eval(dico[src])
            i = 0
            while(i<len(source_list) and not stop):
                element = source_list[i]
                if(element == cible):
                    parents[element] = src
                    stop = True
                elif(element not in explored):
                    parents[element] = src
                    explored.append(element)
                i = i + 1   
        if(stop):
            return chemin_parent(parents,source,cible)
        return []
    except KeyError as e:
        print("la cle n'existe pas sur le wiki")
        return []
    
def pcc_voyelles(source,cible):
    try:
        dico = chg_dico("test_graph.txt")
        sommet_weights = intialiser_graphe(dico,source)
        parents = {}
        explored = [source]
        sommets_visited = [source]
        while(len(explored)>0):
            src = explored.pop(0)
            if(src in dico):
                source_list = eval(dico[src])
                for sommet in source_list:
                    if(sommet_weights[sommet]>(sommet_weights[src]+poids_chemin(sommet))):
                        sommet_weights[sommet] = sommet_weights[src]+poids_chemin(sommet)
                        parents[sommet] = src   
                    if(sommet not in sommets_visited):
                        sommets_visited.append(sommet)
                        explored.append(sommet)
        if(sommet_weights[cible]==float('inf')):
            return []
        return chemin_parent(parents,source,cible) 

    except KeyError as e:
        print("not found")
        
def intialiser_graphe(dico,source):
    init_weights = {}
    init_weights[source] = 0
    explored = [source]
    while(len(explored)>0):
        src = explored.pop(0)
        if(src in dico):
            source_list = eval(dico[src])
            for sommet in source_list:
                if(sommet not in init_weights and sommet not in explored):
                    init_weights[sommet] = float('inf')
                    explored.append(sommet)
    return init_weights

def chemin_parent(parents,source,cible):
    result = [cible]
    parent = cible
    while(parent != source):
        parent = parents[parent]
        result.insert(0,parent)
    return result
def poids_chemin(sommet):
    poids = 1
    result = 0
    for i in range(0,len(sommet)):
        if (sommet[i] == 'a') or (sommet[i] == 'e') or (sommet[i] == 'i') or (sommet[i] == 'o') or (sommet[i] == 'u') or (sommet[i] == 'y'):
            poids = 2
        else:
            poids = 1
        result = result + poids
    return result  
def liste_personnages():
    liste = []
    for letter in string.ascii_uppercase:
        url = "https://iceandfire.fandom.com/wiki/Category:Characters?from="
        url +=letter
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.find_all('li', class_='category-page__member'):
            nom = li.text.strip()
            if nom != "" and nom is not None:
                liste.append(nom)
    return liste
def representation_personnages():
    personnages = liste_personnages()
    dic = {}
    for personnage in personnages:
        temp_list = []
        print(personnage)
        response = requests.get("https://iceandfire.fandom.com"+prefix+personnage)
        soup = BeautifulSoup(response.text, 'html.parser')
        father_section = soup.find('h3',string="Father")
        if(father_section != None):
            father_div = father_section.next_sibling.next_sibling
            for person in father_div.find_all('a'):
                temp_list.append((person.text,1))
                
        mother_section = soup.find('h3',string="Mother")
        if(mother_section != None):
            mother_div = mother_section.next_sibling.next_sibling
            for person in mother_div.find_all('a'):
                temp_list.append((person.text,1))
                    
        children_section = soup.find('h3',string="Children")
        if(children_section != None):
            children_div = children_section.next_sibling.next_sibling
            for person in children_div.find_all('a'):
                temp_list.append((person.text,1))
                
        lover_section = soup.find('h3',string="Lover")
        if(lover_section != None):
            lover_div = lover_section.next_sibling.next_sibling
            for person in lover_div.find_all('a'):
                temp_list.append((person.text,3))
        
        spouse_section = soup.find('h3',string="Spouse")
        if(spouse_section != None):
            spouse_div = spouse_section.next_sibling.next_sibling
            for person in spouse_div.find_all('a'):
                temp_list.append((person.text,3))
                
        siblings_section = soup.find('h3',string="Siblings")
        if(siblings_section != None):
            siblings_div = siblings_section.next_sibling.next_sibling
            for person in siblings_div.find_all('a'):
                temp_list.append((person.text,5))
        dic[personnage] = temp_list
    svg_dico(dic, "personnages.txt")        
    return dic
                
        
#print(plus_court_chemin("abdelhak", "son"))
#print(pcc_voyelles("abdelhak","son"))  
             
print(representation_personnages())
    
    

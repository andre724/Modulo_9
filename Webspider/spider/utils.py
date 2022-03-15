from spider.Graph import Graph, Node
from bs4 import BeautifulSoup as bs
from spider.Similarity import Similarity
import numpy as np
import requests
import os
import re

def main_func(url,cont,Urls,marker,main_dic,relations):
    '''Função principal chamada na view'''
    get_relations=crawler(url,5,Urls,1,main_dic,relations)
    dataset_name=dataset_maker(url, get_relations[2])
    decay_factor = 0.9
    iteration = 100

    graph = init_graph(dataset_name[0])
    sim = Similarity(graph, decay_factor)

    SimRank(graph, sim, iteration)
    ans = sim.get_sim_matrix()
    print(ans)
    
    
    clean_name= dataset_name[1]
    path= os.getcwd()
    path= path + '\Webspider\spider\SimRank_results'
    simrank_path= f'{path}\{clean_name}SimRank.txt'
    np.savetxt(simrank_path, ans, delimiter=' ', fmt='%.2f')

    orded_list= matrix_process(get_relations[1], simrank_path)
    results=[]
    for i in orded_list:
        results.append(i[1])
    return results

def crawler(url,cont,Urls,marker,main_dic,relations):   
    '''Essa é a função que entra no url requisitado, pega os links e marca a relação pai e filho'''
    if cont == 0:
        
        return Urls, main_dic,relations
    else:
        r= requests.get(url)
        if url not in main_dic:
            main_dic[url]= marker
            marker+=1

        pathUrl = url.split('/')[2]
        soup= bs(r.content, 'html.parser')
        urls= soup.find_all('a', href = True)
        for link in urls:
            clean_link=link.attrs["href"]
            if clean_link[:1] == '/':
                    aux = f'https://' + pathUrl+clean_link
            elif 'https://' in clean_link or 'http://' in clean_link:
                    aux = clean_link
            elif clean_link[:1] == '#':
                continue
            else:
                continue
            if aux not in main_dic and aux != url:
                main_dic[aux]= marker
                marker+=1
                auxtuple= (main_dic[url], main_dic[aux])
                relations.append(auxtuple)
                if aux not in Urls:
                    a = crawler(aux, cont-1, Urls, marker,main_dic,relations)
            Urls.add(aux)
            print(relations)
        
            
                
            
        return Urls,main_dic,relations

    


def dataset_maker(url,relations):
    '''Função que cria o dataset que é usado pelo algoritimo SimRanK'''
    
    relation_list= relations
    clean_name= url[8:-1] 
    path= os.getcwd()
    path= path + '\Webspider\spider\datasets'
    dataset_path= f'{path}\{clean_name}dataset.txt'
    if  os.path.isfile(dataset_path) == False:
        with open(dataset_path, 'a') as dataset:
            for i in relation_list:
                dataset.writelines(f'{i[0]},{i[1]}\n')
        return dataset_path
    else:
        return dataset_path, clean_name
                

        
def init_graph(fname):
    with open(fname) as f:
        lines = f.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)

    graph.sort_nodes()

    return graph
    


def SimRank_one_iter(graph, sim):
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            new_SimRank = sim.calculate_SimRank(node1, node2)
            sim.update_sim_value(node1, node2, new_SimRank)
            # print(node1.label, node2.label, new_SimRank)

    sim.replace_sim()


def SimRank(graph, sim, iteration=100):
    for i in range(iteration):
        SimRank_one_iter(graph, sim)
        # ans = sim.get_sim_matrix()
        # print(ans)
        # print()


def matrix_process(main_dic,simrank_path):
    '''Função que processa a matrix criada pelo algoritimo'''
    cont= 1
    sorted_results= dict()
    marker_sum= dict()
    aux_list=[]
    with open(simrank_path,"r") as t:
        for line in t:
            p = re.compile(r'\d+\.\d+')
            aux_list = [float(i) for i in p.findall(line)] 
            aux_array=np.array(aux_list)  
            marker_sum[cont]= np.sum(aux_array)
            cont+=1

    for i in marker_sum:
        for a in main_dic:
            if i == main_dic[a]:
                sorted_results[a]=marker_sum[i]

    
    return sorted(sorted_results.items(), key=lambda item: item[1], reverse=True)
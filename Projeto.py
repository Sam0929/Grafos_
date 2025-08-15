"""
Programa para resolver um desafio relacionado a grafos em Python.

Autores: Samuel, Gabriel, Enzo, Guilherme
Data: 15/08/2025

"""

import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np

MATRIZ = [  #Assumir 1=Círculo, 2=Quadrado, 3=Triangulo, 4=Estrela
    [2,3,1,3,1,2],
    [3,3,2,1,2,3],
    [1,2,3,2,3,1],
    [3,1,2,2,3,3],
    [1,2,3,2,3,1],
    [2,3,1,1,2,3]
]
MATRIZ2 = [  #Assumir 1=Círculo, 2=Quadrado, 3=Triangulo, 4=Estrela
    [2,3,1,3,1,2,1,2,1],
    [3,3,2,1,2,3,2,1,3],
    [1,2,3,2,3,1,3,3,2],
    [3,1,2,2,3,3,2,2,3],
    [1,2,3,2,3,1,1,3,2],
    [2,3,1,1,2,3,2,1,1],
    [2,3,1,3,1,2,1,2,1],
    [3,3,2,1,2,3,2,1,3],
    [1,2,3,2,3,1,3,3,2],
    [3,1,2,2,3,3,2,2,3],
    [1,2,3,2,3,1,1,3,2],
    [2,3,1,1,2,3,2,1,1]
]
MATRIZ = MATRIZ2

#FUNCOES 

def draw_edges (edge_list, color):

    for edge in edge_list:

        weight = G[edge[0]][edge[1]]['weight']
        if weight > 1:
            nx.draw_networkx_edges(G, pos = rotated_pos_nodes, edgelist=[edge], edge_color=color, connectionstyle=f'arc3,rad={weight /10:.2f}')
        else:
            nx.draw_networkx_edges(G, pos = rotated_pos_nodes, edgelist=[edge], edge_color=color)

#DICIONARIO DE POSICOES, CONTEM OS NOMES (C,S,T) COMO CHAVE E AS POSICOES CORRESPONDENTES EM UMA LISTA

positions = {'circle': [], 'square': [], 'triangle': []}

for i, lista in enumerate (MATRIZ):
    for j, num in enumerate (lista):
        if(num == 1):
            positions['circle'].append((i,j))
        
        elif(num == 2):
            positions['square'].append((i,j))
        
        elif(num == 3):
            positions['triangle'].append((i,j))

#DICIONARIO PARA TRADUZIR POSICAO EM NODE

pos_nodes = {}                      
count = 0
for i in range(len(MATRIZ)):
    for j in range(len(MATRIZ[0])):
        pos_nodes[(i,j)] = count
        count += 1

#CRIANDO UM DICIONARIO PARA ROTACIONAR AS POSICOES E EXIBIR O GRAFO COMO NO DESAFIO

rotated_pos_nodes = {}

num_rows = len(MATRIZ)

for (i,j), value in pos_nodes.items():
    rotated_pos_nodes[value] = (j, num_rows - 1 - i)

#CRIANDO O DIGRAFO E ADICIONANDO OS NOS

G = nx.DiGraph()                                
G.add_nodes_from(pos_nodes.values())

#LISTAS PARA ADICIONAR AS ARESTAS

circle_to_square_edge_list = []

square_to_triangle_edge_list = []

triangle_to_square_edge_list = []


#INICIO DOS CALCULOS PARA SEGUIR A LOGICA DO DESAFIO

#CALCULANDO TODAS AS LIGACOES  CIRCULO -> QUADRADO

positions_square = {}
next_square = []

for circle in positions['circle']:

    dist_from_square = float("inf")  
    closest_squares = []             

    for square in positions['square']:
        dist = math.sqrt((circle[0] - square[0]) ** 2 + (circle[1] - square[1]) ** 2)

        if dist < dist_from_square:

            dist_from_square = dist
            closest_squares = [square]

        elif dist == dist_from_square:
            
            closest_squares.append(square)

    positions_square[circle] = closest_squares
    next_square += closest_squares

    for square in closest_squares:
        edge = (pos_nodes[circle], pos_nodes[square])
        G.add_edge(*edge, color='green', weight = dist_from_square)
        circle_to_square_edge_list.append(edge)

# print(f"Essas são as posições dos quadrados:", positions_square)

#CALCULANDO TODAS AS LIGACOES QUADRADO -> TRIANGULO

positions_triangle = {}
next_triangle = []

for square in next_square:

    dist_from_triangle = float("inf")  
    closest_triangles = []
    
    coord_x = square[0]
    coord_y = square[1]             

    for triangle in positions['triangle']:

        dist = abs(triangle[0] - square[0])  + abs(triangle[1] - square[1])

        if triangle[0] >= coord_x and triangle[1] >= coord_y:

            if dist < dist_from_triangle:
                
                    dist_from_triangle = dist
                    closest_triangles = [triangle]

            elif dist == dist_from_triangle:
                
                    closest_triangles.append(triangle)

    positions_triangle[square] = closest_triangles
    next_triangle += closest_triangles

    for triangle in closest_triangles:
        edge = (pos_nodes[square], pos_nodes[triangle])
        G.add_edge(*edge, color='black', weight = dist_from_triangle)
        square_to_triangle_edge_list.append(edge)

# print(f"Essas são as posições dos triângulos:", positions_triangle) 

#CALCULANDO TODAS AS LIGACOES TRIANGULO -> QUADRADO_FINAL

positions_final = {}

for triangle in next_triangle:
    
    dist_from_square = float("inf")
    closest_squares = []

    for square in positions ['square']:

        dist = abs(square[0] - triangle[0])  + abs(square[1] - triangle[1])

        if (abs(triangle[0] - square[0]) == abs(triangle[1] - square[1])):

            if dist < dist_from_square:

                dist_from_square = dist
                closest_squares = [square]

            elif dist == dist_from_square:

                closest_squares.append(square)

    positions_final[triangle] = closest_squares

    for square in closest_squares:
        edge = (pos_nodes[triangle], pos_nodes[square])
        G.add_edge(*edge, color='blue', weight = dist_from_square)
        triangle_to_square_edge_list.append(edge)

# print(f"Essas são as posições dos quadrados depois dos triangulos:", positions_final) 

#LISTAS PARA QUE CONTEM OS NOS DE CADA FORMA, NECESSARIO PARA DESENHAR

circle_nodes = []
square_nodes = []
triangle_nodes = []
star_nodes = []

for value_list in positions_final.values():
    for value in value_list:
        star_nodes.append(pos_nodes[value]) 

count = 0

for i in range(len(MATRIZ)):
    for j in range (len(MATRIZ[0])):
        if MATRIZ[i][j] == 1:
            circle_nodes.append(count)
        elif MATRIZ[i][j] == 2:
            square_nodes.append(count)
        elif MATRIZ[i][j] == 3:
            triangle_nodes.append(count)
        count += 1

# DESENHANDO OS NOS

nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=circle_nodes, node_size=300, node_color="#12be20", node_shape='o')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=square_nodes, node_size=300, node_color="#000000", node_shape='s')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=triangle_nodes, node_size=300, node_color="#1e12be", node_shape='^')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=star_nodes, node_size=300, node_color='gold', node_shape='*')

# DESENHANDO AS ARESTAS

draw_edges(circle_to_square_edge_list, 'green')
draw_edges(square_to_triangle_edge_list, 'black')
draw_edges(triangle_to_square_edge_list, 'blue')



# EXIBINDO O GRAFO

manager = plt.get_current_fig_manager()
manager.window.state('zoomed')

plt.show()


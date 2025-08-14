import networkx as nx
import matplotlib.pyplot as plt
import math

numberToLetter = {1:'C',2:'Q',3:'T',4:'E'}
# Sigam os seguintes passosa
# :
# 1 Escolher 1 qualquer
# 2 Ir para o 2 mais próximo
# 3 Ir para o 3 mais próximo,apenas à direita ou abaixo do quadrado
# 4 Ir para o 2 mais próximo,
# apenas diagonais
# 5 Perguntar ao colega do lado o ponto
# de chegada
# aEm caso de empate escolham livre

# G = nx.Graph()
# nx.draw(G, with_labels=True)
# plt.show()
# print("estou aqui")
MATRIZ = [  #Assumir 1=Círculo, 2=Quadrado, 3=Triangulo, 4=Estrela
    [2,3,1,3,1,2],
    [3,3,2,1,2,3],
    [1,2,3,2,3,1],
    [3,1,2,2,3,3],
    [1,2,3,2,3,1],
    [2,3,1,1,2,3]
]

positions = {'circle': [], 'square': [], 'triangle': []}

for i, lista in enumerate (MATRIZ):
    for j, num in enumerate (lista):
        if(num == 1):
            positions['circle'].append((i,j))
        
        elif(num == 2):
            positions['square'].append((i,j))
        
        elif(num == 3):
            positions['triangle'].append((i,j))

pos_nodes = {}
count = 0
print(len(MATRIZ[0]))
for i in range(len(MATRIZ)):
    for j in range(len(MATRIZ[0])):
        pos_nodes[(i,j)] = count
        count += 1

print(pos_nodes)


rotated_pos_nodes = {}
num_rows = len(MATRIZ)
num_cols = len(MATRIZ[0])

for (i,j), value in pos_nodes.items():
    rotated_pos_nodes[value] = (j, num_rows - 1 - i)

G = nx.DiGraph()
G.add_nodes_from(pos_nodes.values())

print(type(pos_nodes))
print ('Aqui sao os valores',pos_nodes.values())

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

print(f"Essas são as posições dos quadrados:", positions_square)

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

print(f"Essas são as posições dos triângulos:", positions_triangle)

positions_final = {}

for triangle in next_triangle:
    
    dist_from_square = float("inf")
    closest_squares = []

    for square in positions ['square']:

        dist = abs(square[0] - triangle[0])  + abs(square[1] - triangle[1])

        if ((triangle[0] + triangle [1] - square[0] + square[1]) % 2 == 0):

            if dist < dist_from_square:

                dist_from_square = dist
                closest_squares = [square]

            elif dist == dist_from_square:

                closest_squares.append(square)

    positions_final[triangle] = closest_squares

print(f"Essas são as posições dos quadrados depois dos triangulos:", positions_final)

circle_to_square_edge_list = []
for key, value_list in positions_square.items():
    for value in value_list:
        edge = (pos_nodes[key], pos_nodes[value])
        G.add_edge(*edge, color='green')
        circle_to_square_edge_list.append(edge)

square_to_triangle_edge_list = []
for key, value_list in positions_triangle.items():
    for value in value_list:
        edge = (pos_nodes[key], pos_nodes[value])
        G.add_edge(*edge, color='black')
        square_to_triangle_edge_list.append(edge)

triangle_to_square_edge_list = []
for key, value_list in positions_final.items():
    for value in value_list:
        edge = (pos_nodes[key], pos_nodes[value])
        G.add_edge(*edge, color='blue')
        triangle_to_square_edge_list.append(edge)


print (circle_to_square_edge_list)
print (square_to_triangle_edge_list)
print (triangle_to_square_edge_list)


circle_nodes = []
square_nodes = []
triangle_nodes = []
star_node = next(iter(positions_final.values()))[0]  #qualquer valor da posicao final e valida

count = 0
for i in range(6):
    for j in range (6):
        if MATRIZ[i][j] == 1:
            circle_nodes.append(count)
        elif MATRIZ[i][j] == 2:
            square_nodes.append(count)
        elif MATRIZ[i][j] == 3:
            triangle_nodes.append(count)
        count += 1
               

nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=circle_nodes, node_size=300, node_color="#12be20", node_shape='o')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=square_nodes, node_size=300, node_color="#000000", node_shape='s')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=triangle_nodes, node_size=300, node_color="#1e12be", node_shape='^')
nx.draw_networkx_nodes(G, pos = rotated_pos_nodes, nodelist=[pos_nodes[star_node]], node_size=300, node_color='gold', node_shape='*')

nx.draw_networkx_edges(G, pos = rotated_pos_nodes, edgelist=circle_to_square_edge_list, edge_color='green')
nx.draw_networkx_edges(G, pos = rotated_pos_nodes, edgelist=square_to_triangle_edge_list, edge_color='black')
nx.draw_networkx_edges(G, pos = rotated_pos_nodes, edgelist=triangle_to_square_edge_list, edge_color='blue', connectionstyle='arc3,rad=0.2')


plt.show()



# |x1-x2| + |y1-y2| 
# #distancia de manhatta
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

positions = {123}

print(type(positions))

positions = {'circle': [], 'square': [], 'triangle': []}

for i, lista in enumerate (MATRIZ):
    for j, num in enumerate (lista):
        if(num == 1):
            positions['circle'].append((i,j))
        
        elif(num == 2):
            positions['square'].append((i,j))
        
        elif(num == 3):
            positions['triangle'].append((i,j))

positions_square = {}

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

print(f"Essas são as posições dos quadrados:", positions_square)


positions_triangle = {}

for square in positions['square']:

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

print(f"Essas são as posições dos triângulos:", positions_triangle)

positions_final = {}

for triangle in positions['triangle']:
    
    dist_from_square = float("inf")
    closest_squares = []

    for square in positions ['square']:

        dist = abs(square[0] - triangle[0])  + abs(square[1] - triangle[1])

        if triangle[0] != square[0] and triangle[1]!= square[1]:

            if dist < dist_from_square:

                dist_from_square = dist
                closest_squares = [square]

            elif dist == dist_from_square:

                closest_squares.append(square)

    positions_final[triangle] = closest_squares

print(f"Essas são as posições dos quadrados depois dos triangulos:", positions_final)

# |x1-x2| + |y1-y2| 
# #distancia de manhattan
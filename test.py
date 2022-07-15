import numpy as np
import random

def gen_heuristic_map(matrix):
    score = 0
    map = []
    for i in range(len(matrix)):
        map.append([])
        for j in range(len(matrix[i])):
            map[i].append(score)
            if score == 0:
                score = 2
            else:
                score *= 2
    
    return np.array(map)



def heuristic(matrix):
    heuristic_map = gen_heuristic_map(matrix)
    SCALE_FACTOR = 0.0001

    # Sort in descending orden and generate a vector with said values
    sorted_values = np.sort(np.array(matrix).flatten())[::-1]
    # Number of non-empty tiles
    tile_count_score = np.count_nonzero(sorted_values)

    board_score = np.multiply(matrix,heuristic_map).sum()
            
    total_score = SCALE_FACTOR * board_score / tile_count_score

    return board_score


def add_four(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 4
    return mat


heuristic([[2, 0, 0, 0], [0, 4, 0, 2], [0, 0, 4, 4], [0, 4, 4, 8]])
heuristic([[2, 0, 0, 0], [0, 4, 0, 2], [0, 0, 4, 4], [0, 4, 4, 8]])

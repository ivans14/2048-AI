import numpy as np
from queue import PriorityQueue
import random as rand
import logic, puzzle
import constants as c


##################################
# REQUIREMENTS
# 
# 1. Heuristic function with objeective value on the board
# 2. Probabilistic function on possible outcomes (where a number might appear)
# 3. Maximazing probabilistic states between the 4 different legal moves
##################################
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


def zero_pos(matrix):
    index_list = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0:
                pos = (i, j)
                index_list.append(pos)

    return index_list
                

def expectimax(matrix, moves, depth, end=False):
    if end:
        return end

    open_set = PriorityQueue()

    for key in moves.keys(): 
        new_matrix, done = moves[key](matrix) # Move matrix
        if done:
            zero_idx = zero_pos(new_matrix)
            temp_scores = []
            for pos in zero_idx:

                new_matrix_two = logic.add_two_idx(new_matrix, pos[0],pos[1])
                
                if depth == 1:
                    score2 = heuristic(new_matrix_two) 
                    del  new_matrix_two
                else:
                    _, score2 = expectimax(new_matrix_two, moves, depth-1)
                    print('a')
                    del new_matrix_two

                temp_scores.append(0.9*score2)

                
        avg_score = np.array(temp_scores).mean() # Avg. all posible scenarios
        open_set.put((-avg_score, avg_score, key))

    return open_set.get()[2], open_set.get()[1]
"""    for key in moves.keys(): 
        new_matrix, done = moves[key](matrix) # Move matrix
        if done:
            zero_idx = zero_pos(new_matrix)
            temp_scores4=[]
            for pos in zero_idx:
                new_matrix_four = logic.add_four_idx(new_matrix, pos)
                if depth == 1:
                    score4=  heuristic(new_matrix)  
                    del new_matrix_four
                else:
                    _, score4 = expectimax(new_matrix_four, moves, depth-1)
                    del new_matrix_four
                temp_scores4.append(0.1*score4)
    
    for i in range(len(temp_scores)):
        avg_score=[]
        avg_score.append(temp_scores[i]+temp_scores4[i])
"""



# Take bottom right as highest heuristic value for highest value for easiest computation
# all corners would work
def heuristic(matrix):
    heuristic_map = gen_heuristic_map(matrix)
    SCALE_FACTOR = 0.0001

    # Sort in descending orden and generate a vector with said values
    sorted_values = np.sort(np.array(matrix).flatten())[::-1]
    # Number of non-empty tiles
    tile_count_score = np.count_nonzero(sorted_values)

    board_score = np.multiply(matrix,heuristic_map).sum()
            
    total_score = SCALE_FACTOR * board_score / tile_count_score

    return total_score


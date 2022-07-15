import numpy as np
from queue import PriorityQueue
import random as rand
import expectimax as exp
import logic, puzzle
import constants as c
from sys import maxsize as MAX



def zero_pos(matrix):
    index_list = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0:
                pos = (i, j)
                index_list.append(pos)

    return index_list

def getAvailableMovesForMin(matrix):
        places = []
        for i in range(4):
            for j in range(4):
                if matrix[i][j] == 0:
                    places.append((i, j, 2))
                    places.append((i, j, 4))
        return places




def maximize(matrix,moves,depth,a,b,end=False):
    MaxUt=-1

    if depth==0:
        return None, heuristic(matrix)


    for key in moves.keys():
        new_matrix, done = moves[key](matrix)
        
        _,score=minimize(new_matrix,moves,depth-1,a,b,end=False)
        print(score)
        
        if score>MaxUt:
            MaxUt=score
            max_child=new_matrix
        if MaxUt>b:
            break

        if MaxUt>a:
            a=MaxUt

    return max_child, heuristic(matrix)
            
        
            


def minimize(matrix,moves,depth,a,b,end=False):
    minUt=MAX
    ind=getAvailableMovesForMin(matrix)
    if depth==0:
        return None, heuristic(matrix)

    for i in ind:
        if i[2]==4:
            new_matrix=logic.add_four_idx(matrix,i[0],i[1])
            _,score=maximize(new_matrix,moves,depth-1,a,b,end=False)
            new_matrix[i[0]][i[1]]=0
        elif i[2]==2:
            new_matrix=logic.add_two_idx(matrix,i[0],i[1])
            _,score=maximize(new_matrix,moves,depth-1,a,b,end=False)
            new_matrix[i[0]][i[1]]=0

        if score<minUt:
            minUt=score 
            min_child=new_matrix

        if minUt>b:
            break

        if minUt<b:
            b=minUt


    return min_child, heuristic(matrix)







def getBestMove(matrix, moves, depth):
    child,_ = maximize(matrix,moves,depth,-1, MAX )
    return child


def move_to_best(matrix,child):
    if logic.up(matrix)[0]==child:
        return logic.up(matrix)
    if logic.down(matrix)[0]==child:
        return logic.down(matrix)
    if logic.left(matrix)[0]==child:
        return logic.left(matrix)
    if logic.right(matrix)[0]==child:
        return logic.right(matrix)

"""def gen_heuristic_map(matrix):
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
    
    return np.array(map)"""



def heuristic(matrix):
    heuristic_map=np.array([[2**3,2**3,2**1,2**0],
                        [2**4,2**5,2**6,2**7],
                        [2**11,2**10,2**9,2**8],
                        [2**12,2**13,2**14,2**15]])
    SCALE_FACTOR = 0.0001

    # Sort in descending orden and generate a vector with said values
    sorted_values = np.sort(np.array(matrix).flatten())[::-1]
    # Number of non-empty tiles
    tile_count_score = np.count_nonzero(sorted_values)

    board_score = np.multiply(matrix,heuristic_map).sum()
            
    total_score = round(SCALE_FACTOR * board_score / tile_count_score,4)

    return total_score

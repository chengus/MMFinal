import sys
import math
import os
import time

grid = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]

h="h"
w="w"
g="g"

# Solved
starting_map = [[0,0,0,g],
                [w,0,0,0],
                [0,h,0,0],
                [0,0,0,0]]
starting_map = [[h,g,0,0],
                [0,w,0,0],
                [0,0,0,h],
                [0,0,0,0]]
starting_map = [[h,0,g,h],
                [w,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]
starting_map = [[h,0,0,0],
                [0,0,0,0],
                [0,0,w,g],
                [0,0,h,0]]
starting_map = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,h],
                [0,0,w,g]]
starting_map = [[h,0,0,0],
                [0,0,0,0],
                [0,0,w,g],
                [0,0,h,0]]
starting_map = [[h,0,0,0],
                [0,0,0,0],
                [0,0,w,g],
                [0,0,h,0]]
starting_map = [[0,0,0,h],
                [0,w,0,0],
                [0,0,0,g],
                [0,0,h,0]]
starting_map = [[h,0,g,h],
                [w,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]
starting_map = [[0,h,h,0],
                [0,0,0,g],
                [0,0,0,w],
                [0,0,0,h]]
starting_map = [[h,0,0,h],
                [0,h,g,0],
                [0,0,0,0],
                [0,0,w,0]]
starting_map = [[0,0,h,0],
                [w,g,0,0],
                [0,0,0,h],
                [0,0,0,0]]
starting_map = [[0,0,0,0],
                [w,0,g,0],
                [0,0,h,h],
                [0,0,0,0]]
# Not solved

"""
starting_map = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]
"""
#Current
starting_map = [[0,0,0,0],
                [w,0,g,0],
                [0,0,h,h],
                [0,0,0,0]]


rCord=(0,3)
wumpus=None
hole=[]
gold=None

# Surrounding cells from god view
Godbreeze=[]
Godstench=[]
Godglitter=[]

# Surrounding cells from robot view
direction="N"
gotGold=False
path=[]
rBreeze=[]
rStench=[]
rGlitter=[]
possibleHole=[]
possibleWumpus=[]
possibleGold=[]
goldCord=None
wumpusCord=None
safe_spot=set([(0,3),(0,2),(1,3)])
empty_spots=set([(0,3)])
ideal_path=[(0,3),(0,2),(0,1),(0,0),(1,0),(2,0),(3,0),(3,1),(3,2)]
not_explored=[]
wumpusKilled=None

def generate_map():
    global starting_map, wumpus, hole, gold
    for i, row in enumerate(starting_map):
        for j, cell in enumerate(row):
            if cell == "w":
                wumpus = (j, i)
            elif cell == "h":
                hole.append((j, i))
            elif cell == "g":
                gold = (j, i)
    #print("Wumpus:", wumpus)
    #print("Hole:", hole)
    #print("Gold:", gold)

def generate_god_view():
    if wumpus is not None:
        if wumpus[0]+1<4:
            Godstench.append((wumpus[0]+1, wumpus[1]))
        if wumpus[0]-1>=0:
            Godstench.append((wumpus[0]-1, wumpus[1]))
        if wumpus[1]+1<4:
            Godstench.append((wumpus[0], wumpus[1]+1))
        if wumpus[1]-1>=0:
            Godstench.append((wumpus[0], wumpus[1]-1))
    
    for h in hole:
        if h[0]+1<4:
            Godbreeze.append((h[0]+1, h[1]))
        if h[0]-1>=0:
            Godbreeze.append((h[0]-1, h[1]))
        if h[1]+1<4:
            Godbreeze.append((h[0], h[1]+1))
        if h[1]-1>=0:
            Godbreeze.append((h[0], h[1]-1))
    
    if gold[0]+1<4:
        Godglitter.append((gold[0]+1, gold[1]))
    if gold[0]-1>=0:
        Godglitter.append((gold[0]-1, gold[1]))
    if gold[1]+1<4:
        Godglitter.append((gold[0], gold[1]+1))
    if gold[1]-1>=0:
        Godglitter.append((gold[0], gold[1]-1))
    
    Godstench.sort()
    Godbreeze.sort()
    Godglitter.sort()
    
    #print("God view generate")
    #print("Godstench: ", Godstench)
    #print("Godbreeze: ", Godbreeze)
    #print("Godglitter: ", Godglitter)

def print_grid(grid):
    for i in range(4):  # Iterate over the rows of the main grid
        for sub_row in range(2):  # Each 3x3 cell has 3 sub-rows
            row_output = []
            for j in range(4):  # Iterate over the columns of the main grid
                cell = []

                if sub_row == 0:  # Top row for BSG indicators
                    cell.append('B' if (j, i) in Godbreeze else '-')
                    cell.append('S' if (j, i) in Godstench else '-')
                    cell.append('G' if (j, i) in Godglitter else '-')
                elif sub_row == 1:  # Middle row for main item
                    if (j, i) == rCord:
                        cell = ["🤖", "", " "]  # Robot
                    elif (j, i) == wumpus:
                        cell = ["👹", "", " "]  # Wumpus
                    elif (j, i) in hole:
                        cell = ["⛳️", "", " "]  # Hole
                    elif (j, i) == gold:
                        cell = ["🏆", "", " "]  # Gold
                    else:
                        cell = ["-", "-", "-"]
                else:  # Bottom row or empty cells
                    cell = ["-", "-", "-"]

                cell_str = "".join(cell)
                if ((j, i) in possibleHole or (j, i) in possibleWumpus) and (j, i) in possibleGold:
                    cell_str = f"\033[45m{cell_str}\033[0m"  # Purple background
                elif (j, i) in possibleHole:
                    cell_str = f"\033[41m{cell_str}\033[0m"  # Red background
                elif (j, i) in possibleWumpus:
                    cell_str = f"\033[41m{cell_str}\033[0m"  # Red background
                elif (j, i) in possibleGold:
                    cell_str = f"\033[43m{cell_str}\033[0m"  # Yellow background
                elif (j, i) in empty_spots:
                    cell_str = f"\033[42m{cell_str}\033[0m"  # Green background

                row_output.append(cell_str)  

            print("   ".join(row_output))  
        print() 
    time.sleep(1)
    os.system('clear')
    
def neighbour(cord):
    n=[]
    if cord[0]+1<4:
        n.append((cord[0]+1, cord[1]))
    if cord[0]-1>=0:
        n.append((cord[0]-1, cord[1]))
    if cord[1]+1<4:
        n.append((cord[0], cord[1]+1))
    if cord[1]-1>=0:
        n.append((cord[0], cord[1]-1))
    return set(n)

def is_safe(nextCord):
    if not (0 <= nextCord[0] < 4 and 0 <= nextCord[1] < 4):
        return False
    if nextCord in possibleHole or nextCord in possibleWumpus:
        return False
    return True

def turn_robot(target_direction):
    global direction
    DIRECTIONS = ['N', 'E', 'S', 'W']
    # Check if the target direction is valid
    if target_direction not in DIRECTIONS:
        raise ValueError(f"Invalid target direction: {target_direction}")
    
    # Find indices of current and target directions
    current_index = DIRECTIONS.index(direction)
    target_index = DIRECTIONS.index(target_direction)
    
    # Calculate clockwise and counterclockwise distances
    clockwise_distance = (target_index - current_index) % len(DIRECTIONS)
    counterclockwise_distance = (current_index - target_index) % len(DIRECTIONS)
    
    # Choose the optimal direction to turn
    if clockwise_distance <= counterclockwise_distance:
        step = 1  # Clockwise
        turn_type = "right"
    else:
        step = -1  # Counterclockwise
        turn_type = "left"
    
    # Perform turns step by step until the direction matches the target
    while direction != target_direction:
        current_index = (current_index + step) % len(DIRECTIONS)
        direction = DIRECTIONS[current_index]
        # Insert turning robot code here
        #print(f"Robot turned 90° {turn_type} to: {direction} 🔄")

def move_robot(dir):
    global rCord, gotGold, empty_spots, direction, possibleGold
    # 1: up 2: right 3: down 4: left
    nextCord = None
    if dir == 1:  # up
        turn_robot('N')
        nextCord = (rCord[0], rCord[1] - 1)
    elif dir == 2:  # right
        turn_robot('E')
        nextCord = (rCord[0] + 1, rCord[1])
    elif dir == 3:  # down
        turn_robot('S')
        nextCord = (rCord[0], rCord[1] + 1)
    elif dir == 4:  # left
        turn_robot('W')
        nextCord = (rCord[0] - 1, rCord[1])
    elif dir == 0:  # stay
        nextCord = rCord
    else:
        #print("Invalid direction")
        return
    
    # Check if the next coordinates are on the map
    if not (0 <= nextCord[0] <= 3 and 0 <= nextCord[1] <= 3):
        print("Robot out of bound:", nextCord)
        sys.exit()
        return  # Exit the function without updating rCord

    rCord = nextCord  # Now it's safe to update rCord
    
    if rCord in hole:
        print("Robot fell into hole:", rCord)
        sys.exit()
    elif rCord == wumpus:
        print("Robot killed by wumpus:", rCord)
        sys.exit()
    
    else:
        path.append(rCord)
        #print("Path:",path)

    currentFelt={"breeze":[], "stench":[], "glitter":[]}
    if rCord in Godbreeze :
        rBreeze.append(rCord)
        currentFelt["breeze"]=rCord
        #print("Breeze felt at", rBreeze)
    if rCord in Godstench :
        rStench.append(rCord)
        currentFelt["stench"]=rCord
        #print("Stench felt at", rStench)
    if rCord in Godglitter:
        rGlitter.append(rCord)
        currentFelt["glitter"]=rCord
        #print("Glitter found at", rGlitter)
    if len(currentFelt["breeze"])==0 and len(currentFelt["stench"])==0:
        #print("No breeze, stench felt")
        empty_spots=empty_spots|set(neighbour(rCord))
        #print("Empty spots: ", empty_spots)
    update_possibilities(currentFelt)
    print_grid(grid)
    if rCord == gold:
        gotGold = True
        print("Robot found the gold at:", rCord,"✅✅✅✅✅✅")
        #print("Going back to home")
        possibleGold=[]
        # Move back home
        path_taken=path.copy()[::-1]
        optimal_path=find_path_back(path)
        # Validate path back
        if len(set(optimal_path)-set(path))==0 and len(optimal_path)<len(path_taken) and len(optimal_path)>0:
            #print("Optimal path found")
            path_taken=optimal_path.copy()
        #print("Path back: ",path_taken)
        for i,posCord in enumerate(path_taken[1:]):
            move_by_cord(posCord)
            #print("Next cord: ", path_taken[i+1])
            if posCord == (0,3):
                print("Robot got gold and reached home 🏠🏠🏠✅✅✅")
                print("Total moves: ", len(path)-1)
                sys.exit()
                break
        
        sys.exit()
        
    #print("rCord: ", rCord)
    #print("Gold cord: ", goldCord)
    # Burst
    if rCord in rGlitter and gotGold is False:
        print("Gold around 🤑🤑🤑🤑🤑🤑🤑")
        if goldCord is not None:
            move_by_cord(goldCord)
        temp=rCord
        for x in neighbour(temp)-set(path):
            if is_safe(x):
                print("Moving to gold spot: ", x)
                move_by_cord(x)
                if gotGold:
                    break
                move_by_cord(temp)

def update_possibilities(cFelt):
    global path, rBreeze, rStench, rGlitter, possibleHole, possibleWumpus, possibleGold,goldCord, wumpusCord, empty_spots, Godstench,wumpus, Godbreeze, Godglitter, wumpusKilled, not_explored
    # Update possible hole
    rBreeze=list(set(rBreeze))
    for h in rBreeze:
        possibleHole.extend(list(neighbour(h)-set(possibleHole)-set(path)))
        possibleHole=list(set(possibleHole)-set(path)-set(safe_spot)-set(empty_spots))
    # Update possible wumpus
    possibleWumpus=list(set(possibleWumpus))
    if wumpusCord is None:
        if len(rStench)>1:
            temp_set=neighbour(rStench[0])
            for x in rStench[1:]:
                temp_set=temp_set&neighbour(x)
            temp_set=temp_set-set(path)-set(empty_spots)
            #print("Temp set: ", temp_set)
            if len(temp_set)==1:
                wumpusCord=temp_set.pop()
                #print("Wumpus found at: ", wumpusCord)
        else:
            for s in rStench:
                possibleWumpus.extend(list(neighbour(s)))
                #print("Neighbprs",neighbour(s))
                possibleWumpus=set(possibleWumpus)&set(neighbour(s))-set(path)-set(empty_spots)
                possibleWumpus=list(possibleWumpus)
            for pw in possibleWumpus:
                #print("neighbour(pw): ", neighbour(pw))
                #print("set(rStench): ", set(rStench))
                if len(neighbour(pw)&set(path))!=len(rStench):
                    possibleWumpus.remove(pw)
    # Update possible gold
    rGlitter=list(set(rGlitter))
    if len(rGlitter)>0:
        possibleGold=set(neighbour(rGlitter[0]))
        for g in rGlitter[1:]:
            possibleGold&=neighbour(g)
            possibleGold=set(possibleGold)-set(path)-set(empty_spots)
    possibleGold=list(possibleGold)
    if wumpusCord is not None and wumpusCord in possibleGold:
        possibleGold.remove(wumpusCord)
    if len(possibleGold)==1:
        goldCord=possibleGold[0]
        print("Gold found at: ", goldCord)
        
    curCordNeighbor=neighbour(rCord)
    if len(cFelt["breeze"])==0:
        possibleHole=list(set(possibleHole)-curCordNeighbor)
    if len(cFelt["stench"])==0:
        possibleWumpus=list(set(possibleWumpus)-curCordNeighbor)
    if len(cFelt["glitter"])==0:
        possibleGold=list(set(possibleGold)-curCordNeighbor)
    
    if len(possibleWumpus)==1:
        wumpusCord=possibleWumpus[0]
        #print("Wumpus found at: ", wumpusCord)
    
    # Shoot the wumpus
    if wumpusCord is not None and wumpusCord in neighbour(rCord):
        # Face the direction of the wumpus
        directions_map = {
            (0, 1): 'N',
            (1, 0): 'W',
            (0, -1): 'S',
            (-1, 0): 'E'
        }
        dx = rCord[0] - wumpusCord[0]
        dy = rCord[1] - wumpusCord[1]
        #print("dx, dy: ", dx, dy, "wumpusCord: ", wumpusCord, "rCord: ", rCord)
        target_direction = directions_map[(dx, dy)]
        turn_robot(target_direction)
        print_grid(grid)
        #print("xxxxxxxxxxxxxxxxxxxxxxxxx")
        for i, row in enumerate(starting_map):
            for j, cell in enumerate(row):
                if cell == "w":
                    starting_map[i][j]=0
                    empty_spots.add((j, i))
                    wumpusKilled=(j, i)
                    print("Wumpus shot dead at: ", (j, i),"🔫🔫🔫🔫🔫🔫")
                    break
        wumpusCord=None
        possibleWumpus=[]
        Godbreeze=[]
        Godstench=[]
        Godglitter=[]
        wumpus=None
        rStench=[]
        generate_map()
        generate_god_view()
        #print("New map generated")
        update_possibilities(cFelt)
        print("Moving to wumpus spot: ", wumpusKilled)
        move_by_cord(wumpusKilled)
        
    not_explored=list(set(empty_spots)-set(path))
    #print("Not explored: ", not_explored)
        
    possibleHole.sort()
    possibleGold.sort()
    possibleWumpus.sort()
    print("Possible hole: ", possibleHole)
    print("Possible wumpus: ", possibleWumpus)
    print("Possible gold: ", possibleGold)

def move_by_cord(nextCord):
    global rCord
    if rCord[0]==nextCord[0]:
        if rCord[1]<nextCord[1]:
            move_robot(3)
        else:
            move_robot(1)
    else:
        if rCord[0]<nextCord[0]:
            move_robot(2)
        else:
            move_robot(4)

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def point_to_segment_distance_and_projection(point, seg_start, seg_end):
    """
    Calculate the shortest distance from a point to a line segment and the projection of the point onto the segment.
    """
    # Vector from start to end of the segment
    seg_vector = (seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
    # Vector from start of segment to the point
    point_vector = (point[0] - seg_start[0], point[1] - seg_start[1])
    # Calculate the projection factor (t)
    seg_length_squared = seg_vector[0] ** 2 + seg_vector[1] ** 2
    if seg_length_squared == 0:  # Segment start and end are the same
        return euclidean_distance(point, seg_start), seg_start
    t = max(0, min(1, (point_vector[0] * seg_vector[0] + point_vector[1] * seg_vector[1]) / seg_length_squared))
    # Find the projection point
    projection = (seg_start[0] + t * seg_vector[0], seg_start[1] + t * seg_vector[1])
    return euclidean_distance(point, projection), projection

def path_distance_to_point(start, path, point_on_path):
    distance = 0
    for i in range(len(path) - 1):
        seg_start, seg_end = path[i], path[i + 1]
        if point_on_path == seg_start:
            return distance
        if point_on_path == seg_end:
            return distance + euclidean_distance(seg_start, seg_end)
        distance += euclidean_distance(seg_start, seg_end)
    return distance  # Fallback, should not reach here

def closest_point_to_path(points, path):
    closest_point = None
    min_distance = float('inf')
    max_path_distance = -float('inf')
    for point in points:
        for i in range(len(path) - 1):  # Iterate over segments
            distance, projection = point_to_segment_distance_and_projection(point, path[i], path[i + 1])
            if distance < min_distance:
                min_distance = distance
                closest_point = point
                closest_projection = projection
                path_distance = path_distance_to_point(path[0], path, closest_projection)
                max_path_distance = path_distance
            elif distance == min_distance:
                path_distance = path_distance_to_point(path[0], path, projection)
                if path_distance > max_path_distance:
                    closest_point = point
                    closest_projection = projection
                    max_path_distance = path_distance
    return closest_point

def in_loop(max_loop_length=10):
    global path
    if len(path) < max_loop_length:
        return False
    # Check for repeating sequences in the recent positions
    for i in range(1, max_loop_length):
        sequence = path[-i:]
        if len(sequence) * 2 > len(path):
            break
        if sequence == path[-2 * i:-i]:
            return True
    return False

def find_path_back(path_taken):
    # Current position is the last coordinate in the path
    current_pos = path_taken[-1]
    start_pos = (0, 3)
    
    # If already at start, return empty path
    if current_pos == start_pos:
        return []
    
    # Path to return
    path_back = [current_pos]
    
    while current_pos != start_pos:
        # Prefer moving to an existing coordinate in the path
        # Try moving down
        down_pos = (current_pos[0], current_pos[1] + 1)
        if down_pos[1] <= 3 and down_pos in path_taken:
            current_pos = down_pos
            path_back.append(current_pos)
            continue
        
        # Try moving left
        left_pos = (current_pos[0] - 1, current_pos[1])
        if left_pos[0] >= 0 and left_pos in path_taken:
            current_pos = left_pos
            path_back.append(current_pos)
            continue
        
        # If no existing coordinate works, generate a path
        # Prioritize moving towards start point
        if current_pos[0] > 0:
            # Move left
            current_pos = (current_pos[0] - 1, current_pos[1])
            path_back.append(current_pos)
        elif current_pos[1] > 3:
            # Move up
            current_pos = (current_pos[0], current_pos[1] - 1)
            path_back.append(current_pos)
        else:
            # Move down if possible
            if current_pos[1] < 3:
                current_pos = (current_pos[0], current_pos[1] + 1)
                path_back.append(current_pos)
            else:
                # Fallback to moving directly to start point
                break
    
    # Ensure we end at the start point
    if current_pos != start_pos:
        current_pos = start_pos
        path_back.append(current_pos)
    
    return path_back

i=0
if __name__ == "__main__":
    os.system('clear')
    generate_map()
    generate_god_view()
    move_robot(0)
    while not gotGold:
        
        # Trace back to wumpus Useless?
        if wumpusCord is not None:
            #print("Wumpus found, moving backwards")
            temp_path=path.copy()
            #print(temp_path[1::-1])
            #for prevCord in temp_path[1::-1]:
            for prevCord in temp_path[::-1][1:]:
                #print("prevCord: ", prevCord)
                # Check if wumpus is in the next cell
                if wumpusCord is not None and ((abs(rCord[0] - wumpusCord[0]) <= 1 and rCord[1] == wumpusCord[1]) or \
                    (abs(rCord[1] - wumpusCord[1]) <= 1 and rCord[0] == wumpusCord[0])):
                    move_by_cord(wumpusCord)
                else:
                    move_by_cord(prevCord)

        if in_loop():
            print("Robot in loop ⛔️⛔️⛔️⛔️⛔️⛔️")
            #print("Not yet explored: ", not_explored)
            if len(not_explored)>0:
                temp_path=path.copy()
                #print(temp_path[1::-1])
                new=False
                for prevCord in temp_path[::-1][1:]:
                    if new:
                        break
                    #print("prevCord: ", prevCord)
                    #print("Not yet explored neighbors: ", neighbour(prevCord)&set(not_explored))
                    move_by_cord(prevCord)
                    if len(neighbour(prevCord)&set(not_explored))>0:
                        for x in neighbour(prevCord)&set(not_explored):
                            if is_safe(x):
                                move_by_cord(x)
                                new=True
                                break
            else:
                if is_safe((rCord[0], rCord[1]-1)):
                    move_robot(1)
                if is_safe((rCord[0], rCord[1]-1)):
                    move_robot(1)
                elif is_safe((rCord[0]+1, rCord[1])):
                    move_robot(2)
                
        # Follow ideal path
        if rCord in ideal_path and ideal_path.index(rCord)!=len(ideal_path)-1 and is_safe(ideal_path[ideal_path.index(rCord)+1]):
            #print("Following ideal path, next cord: ", ideal_path[ideal_path.index(rCord)+1])
            move_by_cord(ideal_path[ideal_path.index(rCord)+1])
        
        else:
            possible_next_cord = set(neighbour(rCord))-set(path)
            #print("Possible next cords: ", possible_next_cord)
            next_cord=closest_point_to_path(possible_next_cord, ideal_path)
            #print("Closest point to path: ", next_cord)
            
            if next_cord is None:
                #print("No possible next cord, tracing steps")
                temp_path=path.copy()
                #print(temp_path[1::-1])
                for prevCord in temp_path[::-1][1:]:
                    #print("prevCord: ", prevCord)
                    if len(neighbour(prevCord)-set(path))>0:
                        move_by_cord(prevCord)
                        for x in neighbour(prevCord)-set(path):
                            if is_safe(x):
                                move_by_cord(x)
                                break
                    else:
                        move_by_cord(prevCord)
            elif is_safe(next_cord):
                #print("Next cord: ", next_cord)
                move_by_cord(next_cord)
            elif is_safe((rCord[0], rCord[1]+1)):
                #print("Case 1")
                move_robot(3) # Move down
                if is_safe((rCord[0]+1, rCord[1])):
                    #print("Case 1.1")
                    move_robot(2) # Move right
            else:
                #print("Case 2")
                move_by_cord(path[-2])
                if is_safe((rCord[0], rCord[1]+1)):
                    #print("Case 2.1")
                    move_robot(3) # Move down
                if is_safe((rCord[0]+1, rCord[1])):
                    #print("Case 2.2")
                    move_robot(2) # Move right

        """
        i+=1
        if i>30:
            print("Run time exceeded")
            sys.exit()
        """
    
    
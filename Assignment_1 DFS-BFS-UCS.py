# -*- coding: utf-8 -*-
"""
DFS, BFS, UCS searching algorithms with Node constructor class

@author: Sam Hekman
"""
import numpy as np

### Constructor class
class Node:
    def __init__(self, state, depth, cost, prev_node, last_move):
        
        self.state = state              #Game board at this state
        self.depth = depth              #Search tree level at this state
        self.cost = cost                #Total cost reaching this state
        self.prev_node = prev_node      #Parent node of this state
        self.last_move = last_move      #Last move made to reach this state
    
    def get_state(self):
        return self.state
    
    def get_depth(self):
        return self.depth
    
    def get_cost(self):
        return self.cost
    
    def get_prev_node(self):
        return self.prev_node
    
    def get_last_move(self):
        return self.last_move
    
    ### Function for printing the full solution history in order from root to goal
    def solution_path(self):
        
        current_node = self
        # initialize lists of states and corresponding moves
        states = []
        moves = []

        while current_node.prev_node is not None:
            states.insert(0, current_node.get_state().copy())
            moves.insert(0, current_node.get_last_move())
            current_node = current_node.prev_node
            
        
        print("Starting from state:\n")
        # print root node's state
        print_state(current_node.get_state().copy())
        
        while states:
            print("From here, move {}:\n".format(moves.pop(0)))
            print_state(states.pop(0))
        print("\nArrived at solution!")


### Function to print the state in a board layout
def print_state(state):
    print("Current board layout:")
    print("._______.")
    print("| {} {} {} |".format(state[0], state[1], state[2]))
    print("| {} {} {} |".format(state[3], state[4], state[5]))
    print("| {} {} {} |".format(state[6], state[7], state[8]))
    print("---------")
   
    
### Function for returning a list of states at the current node's frontier
### Note: UCS cost is augmented within in the UCS function.
### This adds the cost as +1, as that is the default accross all search types.
def check_frontiers(current_node):
    frontiers = []
    state = current_node.get_state()
    index = state.index(0)
    
    # Check each direction, if moving is impossible, move function returns None
    frontiers.append(Node(move_left(current_node.state, index),
                               current_node.depth + 1,
                               current_node.cost + 1,
                               current_node,
                               "left"))

    frontiers.append(Node(move_up(current_node.state, index),
                               current_node.depth + 1,
                               current_node.cost + 1,
                               current_node,
                               "up"))
    
    frontiers.append(Node(move_right(current_node.state, index),
                               current_node.depth + 1,
                               current_node.cost + 1,
                               current_node,
                               "right"))
    
    frontiers.append(Node(move_down(current_node.state, index),
                               current_node.depth + 1,
                               current_node.cost + 1,
                               current_node,
                               "down"))

    
    # Filter frontier nodes where moving was not possible
    filtered_frontiers = []
    for frontier_node in frontiers:
        if frontier_node.state != None:
            filtered_frontiers.append(frontier_node)
            
    # Return list of frontiers
    return filtered_frontiers
                     
                                  

### Move functions, swaps the 0 with the digit in the movement direction
### These are left, up, down, and right
### Moves are made if legal, otherwise returns None

def move_left(state, index):
    # Get 
    new_state = state.copy()
    # Check legality (won't move off the game board)
    if index not in (0,3,6):
        new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
        return new_state
    # Case that moving is impossible
    else:
        return None

def move_up(state, index):
    new_state = state.copy()
    # Check legality (won't move off the game board)
    if index not in (0,1,2):
        # Swap target index with 0 index
        new_state[index], new_state[index - 3] = new_state[index - 3], new_state[index]
        return new_state
    # Case that moving is impossible
    else:
        return None
        
def move_right(state, index):
    new_state = state.copy()
    # Check legality (won't move off the game board)
    if index not in (2,5,8):
        # Swap target index with 0 index
        new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
        return new_state
    # Case that moving is impossible
    else:
        return None

def move_down(state, index):
    new_state = state.copy()
    # Check legality (won't move off the game board)
    if index not in (6,7,8):
        # Swap target index with 0 index
        new_state[index], new_state[index + 3] = new_state[index + 3], new_state[index]
        return new_state
    # Case that moving is impossible
    else:
        return None



### Helper function for the Uniform Cost Search
### Generates predeterimined cost based on blank tile position and board index
def find_cost(frontier_node):
    
    move = frontier_node.get_last_move()
    
    # Moving left or right costs 2
    if move == "left" or move == "right":
        return 2
    # Moving up or down costs 1
    else:
        return 1



### This function is for serializing the game board (state) into str type,
### allowing the state to be saved to a set for faster exclusivity checks.
def serialize(state):
    srl = ''.join(map(str, state))
    return srl


### Depth First Search function
def depth_first_search(start_state, goal_state, max_depth):
    
    # Initialize a list for a stack for nodes waiting to be explored
    unexplored_states = []
    
    # Add the root node to stack
    unexplored_states.append(Node(start_state, 0, 10, None, "root"))
    
    # set of states to prevent retreading the same paths over and over again
    explored_states = set()
    
    # Give depth limit to prevent infinite deepening
    max_depth = max_depth
    
    solution_found = False
    
    # While there are still unexplored states in the stack
    while unexplored_states:

        # Get the current node from the head of the queue
        current_node = unexplored_states.pop(0)
            
        # Add the current node's state to a list of states
        explored_states.add(serialize(current_node.get_state()))

        # Case that current node's state is the goal state
        if current_node.state == goal_state:
            
            print(current_node.get_cost())
            print("Solution found!\n")
            current_node.solution_path()
            solution_found = True
            # break the loop
            break
        
        # Base case that current node's state is not goal state, and depth limit is not reached    
        elif current_node.depth <= max_depth:
                
            # Generate list of frontiers from current node
            frontiers_list = check_frontiers(current_node)
            
            # Reverse for insertion, keeping left, up, right, down bias
            frontiers_list.reverse()
                
            for frontier in frontiers_list:
                    
                # Serialize frontier node's state
                state_srl = serialize(frontier.get_state())
                    
                # If state not explored, add frontier to front of queue
                if state_srl not in explored_states:
                        
                    # insert at front of the queue
                    unexplored_states.insert(0, frontier)  
                    
    # All search options exhausted at depth limit
    if solution_found == False:
        print("Could not find solution within a depth of {}.".format(max_depth))
    
        
### Breadth First Search function
def breadth_first_search(start_state, goal_state, max_depth):
    
    # Initialize a list for a queue for nodes waiting to be explored
    unexplored_states = []
    
    # Add the root node to queue
    unexplored_states.append(Node(start_state, 0, 0, None, None))
    
    # set of states to prevent retreading the same paths over and over again
    explored_states = set()
    
    
    max_depth = max_depth

    solution_found = False
    
    while unexplored_states:
        
        # Get the current node from the head of the queue
        current_node = unexplored_states.pop(0)
        # Add the current node's state to a list of states
        explored_states.add(serialize(current_node.get_state())) 
        
        # Case that current node's state is the goal state
        if current_node.state == goal_state:
            print("Solution found!\n")
            current_node.solution_path()
            solution_found = True
            # End loop
            break
        
        elif current_node.get_depth() <= max_depth:
                
            # Generate list of frontiers from current node
            frontiers_list = check_frontiers(current_node)
            
            for frontier in frontiers_list:
                # Serialize frontier node's state
                state_srl = serialize(frontier.get_state())
                    
                # If state not explored, add frontier to front of queue
                if state_srl not in explored_states:
                    
                    # Append at back of the queue
                    unexplored_states.append(frontier)
    
    # All search options exhausted at depth limit
    if solution_found == False:
        print("Could not find solution within a depth of {}.".format(max_depth))             


### Uniform Cost Search function
def uniform_cost_search (start_state, goal_state, max_depth):
    
    # Initialize a list for a queue for nodes waiting to be explored
    unexplored_states = []
    
    # Add the root node to queue
    unexplored_states.append(Node(start_state, 0, 1, None, None))
    
    # set of states to prevent retreading the same paths over and over again
    explored_states = set()
    
    max_depth = max_depth
    
    solution_found = False

    while unexplored_states:
        
        # Get the current node from the head of the queue
        current_node = unexplored_states.pop(0)
        # Add the current node's state to a list of states
        explored_states.add(serialize(current_node.get_state()))
        
        # Case that current node's state is the goal state
        if current_node.state == goal_state:
            print("Solution found!\n")
            current_node.solution_path()
            print("\nTotal cost: {}".format(current_node.get_cost()))
            solution_found = True
            # End loop
            break
        
        elif current_node.get_depth() <= max_depth:
                
            # Generate list of frontiers from current node
            frontiers_list = check_frontiers(current_node)
            
            # Reversed order to make sure that up is inserted ahead of down
            # and left ahead of right.
            frontiers_list.reverse()
            
            cost_ordered_frontiers = []
            
            # Order the frontiers back acsending cost
            for frontier in frontiers_list:
                
                # Find the cost of the move made
                c = find_cost(frontier)
                
                # Update total cost for path
                frontier.cost += c-1
                
                # Insert frontiers from lowest to highest cost
                if c == 1:
                    cost_ordered_frontiers.insert(0, frontier)
                elif c == 2:
                    cost_ordered_frontiers.insert(2, frontier)
                
            for frontier in cost_ordered_frontiers:

                # Serialize frontier node's state
                state_srl = serialize(frontier.get_state())
                    
                # If state not explored, add frontier to front of queue
                if state_srl not in explored_states:
                    
                    # Append cost ordered frontiers
                    unexplored_states.append(frontier)
                    
    # All search options exhausted at depth limit               
    if solution_found == False:
        print("Could not find solution within a depth of {}.".format(max_depth))


### Generates random start state
def random_state():
    # built board of 0 to 9
    random_board = np.arange(9)
    # Shuffle board order
    np.random.shuffle(random_board)
    # Convert to list
    new_board = random_board.tolist()
    return new_board


### Driver function
def main():

    # Depth Limit may be changed with this variable!
    # If taking too long to search, please decrease the value!
    max_depth = 31
    # Goal_state
    goal_state = [1,2,3,8,0,4,7,6,5]
    print("Goal state is:")
    print_state(goal_state)
    
    start_state = random_state()
    print("\nStarting state is:")
    print_state(start_state)
    
    print("\n\n### Depth First Search method ###\n")
    depth_first_search(start_state, goal_state, max_depth)
    print("\n\n### Breadth First Search method ###\n")
    breadth_first_search(start_state, goal_state, max_depth)
    print("\n\n### Uniform Cost Search method ###\n")
    uniform_cost_search(start_state, goal_state, max_depth)
    print("\n### Searching completed! ###\n")
    # Done
    
    
### Safety check!
if __name__ == "__main__":
    main()
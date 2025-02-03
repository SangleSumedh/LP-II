from typing import List
from copy import deepcopy

# Define a class 'Node' to represent the state of the puzzle
class Node:
    def __init__(self, matrix: List[List[int]], g_x: int, goal: List[List[int]]) -> None:
        # Initialize the state with the matrix (puzzle configuration), g_x (cost to reach this state), and the goal state
        self.matrix = matrix
        self.g_x = g_x  # g(x): number of moves taken so far
        self.h_x = 0     # h(x): heuristic value (how far the current state is from the goal state)
        self.f_x = 0     # f(x): f(x) = g(x) + h(x), used to prioritize the node in the search
        self.goal = goal  # The goal configuration
        self.n = 3  # Size of the puzzle (3x3)
        
        # Calculate heuristic value (h(x)) and f(x)
        self.calculate_h_x()
        self.calculate_f_x()

    # Function to locate the position of the blank tile (0)
    def locateZero(self):
        for i, row in enumerate(self.matrix):
            for j, ele in enumerate(row):
                if ele == 0:
                    return (i, j)  # Return the coordinates of the blank tile (0)
    
    # Function to generate all possible child states by moving the blank tile
    def generateChildren(self):
        x, y = self.locateZero()  # Find the position of the blank tile
        possible = [
            (x + 1, y),  # Move blank tile down
            (x, y + 1),  # Move blank tile right
            (x - 1, y),  # Move blank tile up
            (x, y - 1)   # Move blank tile left
        ]
        children: List[Node] = []  # List to store generated child nodes

        # Generate each child by swapping the blank tile with an adjacent tile
        for i, j in possible:
            if i >= 0 and i < self.n and j >= 0 and j < self.n:  # Ensure the new position is within bounds
                child = deepcopy(self.matrix)  # Create a copy of the current matrix (to avoid modifying the current state)
                child[x][y], child[i][j] = child[i][j], child[x][y]  # Swap the blank tile with the adjacent tile
                children.append(Node(child, self.g_x + 1, self.goal))  # Create a new child node and add to the list
        return children
    
    # Function to calculate the heuristic (h(x)): Number of tiles that are not in the goal state
    def calculate_h_x(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.goal[i][j] != self.matrix[i][j]:  # Compare each tile with the goal configuration
                    self.h_x += 1  # Increment the heuristic count if the tile is out of place
        
    # Function to calculate the f(x): f(x) = g(x) + h(x)
    def calculate_f_x(self):
        self.f_x = self.g_x + self.h_x  # Total cost is the sum of the cost to reach the node and the heuristic

    # Function to print the details of the current node state (g(x), h(x), f(x), and the matrix)
    def printNode(self):
        print(f"g(x) = {self.g_x}")
        print(f"h(x) = {self.h_x}")
        print(f"f(x) = {self.f_x}")
        for i, row in enumerate(self.matrix):
            for j, ele in enumerate(row):
                print(ele, end=" ")  # Print the tiles in the matrix
            print()
        print()

# Define the main puzzle-solving class
class Puzzle:
    def __init__(self) -> None:
        # Initialize the puzzle with an empty visited list, expanded list, and 3x3 grid
        self.visited: List[Node] = []  # List of nodes that have already been visited
        self.expanded: List[Node] = []  # List of nodes that have been expanded (to explore next)
        self.n = 3  # Size of the puzzle (3x3)
        self.initial = [[] for _ in range(self.n)]  # Initial state of the puzzle
        self.goal = [[] for _ in range(self.n)]  # Goal state of the puzzle
    
    # Function to take input for a state (initial or goal)
    def input(self, variable):
        print("Enter state.\n0 represents blank tile")
        for i in range(self.n):
            variable[i] = [int(j) for j in input().split(" ")]  # Take input row by row
    
    # Function to solve the puzzle using A* search algorithm
    def solve(self):
        matrices = []  # List to store the matrices that have been visited to avoid revisiting them
        print("Enter initial state")
        self.input(self.initial)  # Get the initial state from the user
        print("Enter goal state")
        self.input(self.goal)  # Get the goal state from the user
        
        print("\nSTART")
        # Create the initial node with g_x = 0 (no moves yet), and the goal state
        current = Node(self.initial, 0, self.goal)
        matrices.append(current.matrix)  # Add the initial matrix to the visited list
        self.expanded.append(current)  # Add the initial node to the list of nodes to be expanded

        # Main loop to solve the puzzle
        while True:
            current = self.expanded.pop(0)  # Pop the node with the lowest f(x) from the expanded list
            if current.h_x == 0:  # If the heuristic is 0, we've reached the goal state
                break
            current.printNode()  # Print the current node's details

            # Generate the children of the current node and add them to the expanded list
            for child in current.generateChildren():
                if child.matrix not in matrices:  # If the child state has not been visited before
                    matrices.append(child.matrix)  # Mark the matrix as visited
                    self.expanded.append(child)  # Add the child node to the expanded list

            self.visited.append(current)  # Mark the current node as visited
            self.expanded.sort(key=lambda x: x.f_x, reverse=False)  # Sort the expanded list based on f(x) in ascending order
        
        current.printNode()  # Print the solution node (goal state)

# Create the puzzle object and solve it
puzzle = Puzzle()
puzzle.solve()

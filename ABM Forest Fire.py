# standard includes
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

# Next we are going to import some specific libraries we will use to get the animation to work cleanly
from IPython.display import display, clear_output
import time


def plotgrid(myarray):
    # Initializes the columns and rows of your board from 0 to the length of your array less 1 (because first column is fires)
    x_range = np.linspace(0, myarray.shape[1] - 1, myarray.shape[1])
    y_range = np.linspace(0, myarray.shape[0] - 1, myarray.shape[0])

    # Creates your x y grid with column and row length x and y range
    x_indices, y_indices = np.meshgrid(x_range, y_range)

    # Defines what tree and fire values are
    tree_x = x_indices[myarray == 1];
    tree_y = y_indices[myarray == 1];
    fire_x = x_indices[myarray == 2];
    fire_y = y_indices[myarray == 2];

    # Plots your x and y tree values and fire values
    plt.plot(tree_x, myarray.shape[0] - tree_y - 1, 'gs', markersize=10)
    plt.plot(fire_x, myarray.shape[0] - fire_y - 1, 'rs', markersize=10)

    # Lets us see one column and row to the left and below our array shape
    plt.xlim([-1, myarray.shape[1]])
    plt.ylim([-1, myarray.shape[0]])

    # Gets rid of tick marks on the axis
    plt.tick_params(axis='both', which='both',
                    bottom=False, top=False, left=False, right=False,
                    labelbottom=False, labelleft=False)


def set_board(board_size=50, f_trees_start=0.5):
    '''
    Creates the initial game board.

    Inputs:
        board_size: length of one edge of the board
        f_trees_start: probability that a given cell is a tree
                       (effectively the tree density)

    Outputs a 2D numpy array with values set to either 0, 1, or 2
        (empty, tree, or fire)
    '''

    # all cells initialized to 'empty' (0) by default
    game_board = np.zeros((board_size, board_size), dtype='int64')

    # loop over board and roll the dice; if the random number is less
    # than f_trees_start, make it a tree.
    for i in range(board_size):
        for j in range(board_size):
            if rand.random() <= f_trees_start:
                game_board[i, j] = 1

    # set the whole left edge of the board on fire. We're arsonists!
    game_board[:, 0] = 2

    return game_board


def advance_board(game_board):
    '''
    Advances the game board using the given rules.
    Input: the initial game board.
    Output: the advanced game board
    '''

    # create a new array that's just like the original one, but initially set to all zeros (i.e., totally empty)
    new_board = np.zeros_like(game_board)

    # loop over each cell in the board and decide what to do.
    for i in range(len(game_board)):
        for j in range(len(game_board)):
            place = game_board[i, j]
            # Now that we're inside the loops we need to apply our rules
            # if the cell was empty last turn, it's still empty.
            if place == 0:
                new_board[i, j] = 0
            # if it was on fire last turn, it's now empty.
            if place == 2:
                new_board[i, j] = 0

            # now, if there is a tree in the cell, we have to decide what to do
            if place == 1:
                # initially make the cell a tree in the new board
                new_board[i, j] = 1
                # If one of the neighboring cells was on fire last turn,
                # this cell is now on fire!
                # Checks if fire is on the farthest left column
                if i > 0:
                    if game_board[i - 1, j] == 2:
                        new_board[i, j] = 2
                # Checks if fire is on the farthest right column
                if i < game_board.shape[0] - 1:
                    if game_board[i + 1, j] == 2:
                        new_board[i, j] = 2
                # now complete the rest of code! and add comments accordingly!
                if j > 0:
                    if game_board[i, j - 1] == 2:
                        new_board[i, j] = 2
                # Checks if fire is on the farthest right column
                if j < game_board.shape[1] - 1:
                    if game_board[i, j + 1] == 2:
                        new_board[i, j] = 2

    # return the new board
    return new_board


def calc_stats(game_board, start_board):
    '''
    Calculates the fraction of cells on the game board that are
    a tree or are empty.

    Input: a game board

    Output: fraction that's empty, fraction that's covered in trees.
    '''

    # use numpy to count up the fraction that are empty
    frac_empty = np.sum(game_board[game_board == 0]) - np.sum(start_board[start_board == 0])

    # do the same for trees
    frac_tree = np.sum(game_board[game_board == 1]) - np.sum(start_board[start_board == 1])

    return frac_empty, frac_tree

# Init variables
start_board = set_board()
f_trees_start = 0.6
board_size = 50

# Set figure plot size to a 10 by 10
fig = plt.figure(figsize=(10, 10))

# Init starting game board with init variables
game_board = set_board(board_size=board_size, f_trees_start=f_trees_start)

# Plot the Init game board
plotgrid(game_board)

# Creates break check start for while loop
on_fire = True

# Start our while loop
while on_fire == True:

    # advnace board one place
    game_board = advance_board(game_board)

    # display game code
    plotgrid(game_board)
    time.sleep(0.01)  # pauses for .01 seconds
    clear_output(wait=True)
    display(fig)
    fig.clear()

    # unpack our game board stats
    frac_empty, frac_trees = calc_stats(game_board, start_board)

    # if the sum of trees and empty cells == 1 no more fire, so exit while loop
    if frac_empty + frac_trees == 1.0:
        on_fire = False

# Close the plot
plt.close()
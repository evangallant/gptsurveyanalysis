"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # If it's the first move of the game, return X
    start_comparison = initial_state()
    if board == start_comparison:
        return X

    # Get the number of each player's moved played already in variables
    number_of_x = 0
    number_of_o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                number_of_x += 1
            elif board[i][j] == O:
                number_of_o += 1

    # If the players have played the same number of turns it's X's turn
    if number_of_x == number_of_o:
        return X

    # If the O player has played one less move than the X player, it's O's turn
    elif number_of_x != number_of_o:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Start by making a copy of the board
    new_board = copy.deepcopy(board)
    whos_turn = player(board)

    # If the action is not possible, raise an exception
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Target square is not empty, unable to make move")

    # If it is, make the move
    elif board[action[0]][action[1]] is EMPTY:
        if whos_turn == X:
            new_board[action[0]][action[1]] = X
            return new_board
        elif whos_turn == O:
            new_board[action[0]][action[1]] = O
            return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # List of winning configurations
    winning_configurations = [
        [(0, 0), (0, 1), (0, 2)],  # Top row
        [(1, 0), (1, 1), (1, 2)],  # Middle row
        [(2, 0), (2, 1), (2, 2)],  # Bottom row
        [(0, 0), (1, 0), (2, 0)],  # Left column
        [(0, 1), (1, 1), (2, 1)],  # Middle column
        [(0, 2), (1, 2), (2, 2)],  # Right column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left to bottom-right
        [(0, 2), (1, 1), (2, 0)]   # Diagonal from top-right to bottom-left
    ]

    # For each configuration of squares in that list, see if all the values are either X or O
    for configuration in winning_configurations:
        # Get the X, O, or EMPTY at the first square of each configuration
        symbol = board[configuration[0][0]][configuration[0][1]]
        # Then see if the remaining values in the current configuration are all the same as the symbol in the first
          # First we check if the first squre is EMPTY - if this condition fails we move to the next configuration
          # Next we see if the symbols for the remaining squares in the current configuration are the same as the symbol in the first using all()
        if symbol is not EMPTY and all(board[row][col] == symbol for (row, col) in configuration):
            return symbol

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or (EMPTY not in board):
        return True

    # Otherwise, return false
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # maximizing_move will look at the board, look at the tree of possible moves and outcomes, and return the move with the best outcome for X
    def maximizing_move(board):
        # Initialize the max eval value to negative 2
        max_eval = -2
        best_move = None
        # Look at each possible move and recursively minmax to find the move that leads to the best outcome
        for move in actions(board):
            # If the next move is a terminal state, update max_eval based on the utility of the board
            if terminal(result(board, move)):
                eval = utility(board)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

            # If there are more moves to be made, recursively minmax until we find a terminal state
            else:
                # Since the next move will be O's, we want to guess their best move, which will enetail minimizing the score.
                # In the recursion, min will call max, and max will call min, meaning we are evaluating best play for both sides
                _, eval = minimizing_move(result(board, move)) # This returns the result of O's best move in response to X's currently evaluated move
                # If O's best responding move leads to a better outcome for us, make that our new best move. Once we've gone through all the moves we'll have the optimal move
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            # Return the best move AND the eval for recursive calling
        return best_move, max_eval


    def minimizing_move(board):
        # Initialize the min eval value to  2
        min_eval = 2
        best_move = None
        # Look at each possible move and recursively minmax to find the move that leads to the best outcome
        for move in actions(board):
            # If the next move is a terminal state, update min_eval based on the utility of the board
            if terminal(result(board, move)):
                eval = utility(board)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

            # If there are more moves to be made, recursively minmax until we find a terminal state
            else:
                _, eval = maximizing_move(result(board, move))
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            # Return the best move
        return best_move, min_eval


    # Path if it's X's turn:
    if player(board) == X:
        best_move, _ = maximizing_move(board)
        return best_move

    # Path if it's O's turn:
    else:
        best_move, _ = minimizing_move(board)
        return best_move
"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    x_count = 0
    o_count = 0
    for row in range(3):
        x_count += board[row].count("X")
        o_count += board[row].count("O")
    return "O" if x_count > o_count else "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    resulting_board = deepcopy(board)
    if action not in actions(resulting_board):
        raise Exception("invalid move")
    resulting_board[action[0]][action[1]] = player(resulting_board)
    return resulting_board
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check for row
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
        # Check for col
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in ["X", "O"]:
        return True
    moves_left = 0
    for i in range(3):
        moves_left += board[i].count(None)
    return True if moves_left == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == "X":
        return 1
    elif game_winner == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == "X":
        utilities = []
        for action in actions(board):
            utilities.append([min_value(result(board, action), -math.inf, math.inf), action])
        utilities.sort(key=lambda x: x[0], reverse=True)
        return utilities[0][1]
    elif player(board) == "O":
        utilities = []
        for action in actions(board):
            utilities.append([max_value(result(board, action), -math.inf, math.inf), action])
        utilities.sort(key=lambda x: x[0])
        return utilities[0][1]
    

# Try to maximise utility from choice of minimisations
def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

# Try to minimise utility from choice of maximisations
def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
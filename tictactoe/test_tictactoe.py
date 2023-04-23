from tictactoe import player, actions, result, winner, terminal, utility, minimax

board1 = [[None, None, None],
          [None, None, None],
          [None, None, None]]
board2 = [[None, None, None],
          [None, "X", None],
          [None, None, None]]
board3 = [[None, None, None],
          [None, "X", "O"],
          [None, None, None]]
board4 = [[None, None, "X"],
          [None, "X", "O"],
          [None, None, None]]
board5 = [[None, None, "X"],
          [None, "X", "O"],
          ["O", None, None]]
board6 = [[None, "X", "X"],
          [None, "X", "O"],
          ["O", None, None]]
board7 = [[None, None, "X"],
          [None, "X", "O"],
          ["X", None, "O"]]
board8 = [[None, "X", "X"],
          [None, "X", None],
          ["O", "O", "O"]]
board9 = [["O", "X", "X"],
          ["X", "X", "O"],
          ["O", "X", "O"]]
board10 = [["O", "X", "X"],
          ["X", "O", "O"],
          ["O", "X", "X"]]


def test_player():
    assert player(board1) == "X"
    assert player(board2) == "O"
    assert player(board3) == "X"
    assert player(board4) == "O"
    assert player(board5) == "X"
    assert player(board6) == "O"


def test_actions():
    assert actions(board5) == {(0, 0), (0, 1), (1, 0), (2, 1), (2, 2)}
    assert actions(board6) == {(0, 0), (1, 0), (2, 1), (2, 2)}


def test_result():
    assert result(board1, (1, 1)) == board2
    assert result(board2, (1, 2)) == board3
    assert result(board3, (0, 2)) == board4
    assert result(board4, (2, 0)) == board5
    assert result(board5, (0, 1)) == board6


def test_winner():
    assert winner(board1) == None
    assert winner(board6) == None
    assert winner(board7) == "X"
    assert winner(board8) == "O"
    assert winner(board9) == "X"
    assert winner(board10) == None


def test_terminal():
    assert terminal(board1) == False
    assert terminal(board2) == False
    assert terminal(board3) == False
    assert terminal(board4) == False
    assert terminal(board5) == False
    assert terminal(board6) == False
    assert terminal(board7) == True
    assert terminal(board8) == True
    assert terminal(board9) == True
    assert terminal(board10) == True


def test_utilty():
    assert utility(board1) == 0
    assert utility(board2) == 0
    assert utility(board3) == 0
    assert utility(board4) == 0
    assert utility(board5) == 0
    assert utility(board6) == 0
    assert utility(board7) == 1
    assert utility(board8) == -1
    assert utility(board9) == 1
    assert utility(board10) == 0

# Test currently does not function as expected
def test_minimax():
    assert minimax(board4) == (2, 0)
    assert minimax(board6) == (2, 1)
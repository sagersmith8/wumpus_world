from random import random, choice
from board_state import BoardState
from cell import Cell
import cell_types
import directions


def generate_world(board_size, prob_obst, prob_pit, prob_wump):
    """
    Generates a world with the given parameters

    :param board_size: desired size of the board
    :type board_size: int
    :param prob_obst: probability of an obsticle
    :type prob_obst: float
    :param prob_pit: probability of a pit
    :type prob_pit: float
    :param prob_wump: probability of a wumpus
    :type prob_wump: float
    :rtype: [[Cell]] or None
    :return: [[Cell]] if valid input otherwise None
    """
    if valid_input(board_size, prob_obst, prob_pit, prob_wump):
        return create_board(board_size, prob_obst, prob_pit, prob_wump)


def create_board(board_size, prob_obst, prob_pit, prob_wump):
    """
    Creates a board with the given constraints

    :param board_size: size of the board
    :type board_size: int
    :param prob_obst: probability of an obstical
    :type prob_obst: float
    :param prob_pit: probability of a pit
    :type prob_pit: float
    :param prob_wump: probability of a wumpus
    :type prob_wump: float
    :rtype: [[Cell]]
    :return: an initial board state having the given constraints
    """
    prob_pit += prob_obst
    prob_wump += prob_pit
    while True:
        board = list()
        empty_cells = list()
        for row in xrange(board_size):
            board.append(list())
            for col in xrange(board_size):
                cell = create_cell(prob_obst, prob_pit, prob_wump)
                if cell.cell_type == cell_types.EMPTY:
                    empty_cells.append([row, col])
                board[row].append(cell)
        if len(empty_cells) >= 2:
            place_in_empty_cell(board, cell_types.GOLD, empty_cells)
            starting_pos = choose_empty_cell(empty_cells)
            starting_direction = choose_direction()

            return BoardState(
                board=board,
                pos=starting_pos,
                direction=starting_direction
            )


def place_in_empty_cell(board, cell_type, empty_cells):
    """
    Places a cell of given type in a random empty cell

    :param board: board to place cell_type in
    :type board: [[Cell]]
    :param cell_type: the type of the cell
    :type cell_type: int
    :param empty_cells: a list of empty cells
    :type empty_cells: list
    :rtype: None
    :return: None
    """
    row, col = choose_empty_cell(empty_cells)
    board[row][col] = Cell(cell_type)


def choose_empty_cell(empty_cells):
    """
    Chooses an empty cell and removes it from the set

    :param empty_cells: list of empty cells
    :type empty_cells: tuple
    :rtype: tuple
    :return: Chooses an empty cell
    """
    empty_cell = choice(empty_cells)
    empty_cells.remove(empty_cell)
    return empty_cell


def choose_direction():
    return choice(directions.DIRECTIONS)


def create_cell(prob_obst, prob_pit, prob_wump):
    """
    Creates a cell of the correct type using the probabilities

    :param prob_obst: probability that a cell is of type obstical
    :type prob_obst: float
    :param prob_pit: probability that a cell is of type pit
    :type prob_pit: float
    :param prob_wump: probability that a cell is of type wumpus
    :type prob_wump: float
    :rtype: float
    :return: a Cell of a random type
    """
    cell_type = random()

    if cell_type <= prob_obst:
        return Cell(cell_types.OBSTACLE)
    if cell_type <= prob_pit:
        return Cell(cell_types.PIT)
    if cell_type <= prob_wump:
        return Cell(cell_types.WUMPUS)
    return Cell(cell_types.EMPTY)


def valid_input(board_size, prob_obst, prob_pit, prob_wump):
    """
    Checks if the input to the function is valid

    :param board_size: desired size of the board
    :type board_size: int
    :param prob_obst: probability of an obsticle
    :type prob_obst: float
    :param prob_pit: probability of a pit
    :type prob_pit: float
    :param prob_wump: probability of a wumpus
    :type prob_wump: float
    :rtype: bool
    :return: if the input is valid
    """
    return (
        check_board_size(board_size) and
        check_prob(prob_obst, prob_pit, prob_wump)
    )


def check_board_size(board_size):
    """
    Checks that the board size is valid

    :param board_size: size of the board
    :type board_size: int
    :rtype: bool
    :return: return if the board size is valid
    """
    return 5 <= board_size <= 25


def check_prob(prob_obst, prob_pit, prob_wump):
    """
    Checks that the probabilities are correct

    :param prob_obst: probability of an obsticle
    :type prob_obst: float
    :param prob_pit: probability of a pit
    :type prob_pit: float
    :param prob_wump: probability of a wumpus
    :type prob_wump: float
    :rtype: bool
    :return: return if the probability is correct
    """
    return prob_obst+prob_pit+prob_wump < 1

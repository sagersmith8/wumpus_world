from cell_types import WUMPUS, EMPTY, OBSTACLE, GOLD, PIT


class Cell:
    def __init__(self, cell_type):
        """
        Constructs a cell of the given type

        :param cell_type: the type of the cell to construct
        :type cell_type: int
        :rtype: Cell
        :return: Cell of the given type
        """
        self.percepts = list()
        self.cell_type = cell_type

    def kill(self):
        """
        Checks if the board can be killed and kills it if it can

        :rtype: bool
        :return: True if cell was killed, false if cell was not
        """
        if self.cell_type == WUMPUS:
            self.cell_type = EMPTY
            return True
        return False

    def __str__(self):
        if self.cell_type == WUMPUS:
            return '[W]'
        if self.cell_type == EMPTY:
            return '[E]'
        if self.cell_type == OBSTACLE:
            return '[O]'
        if self.cell_type == GOLD:
            return '[G]'
        if self.cell_type == PIT:
            return '[P]'

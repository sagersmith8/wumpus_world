class Cell:
    """
    Cell types
    """
    EMPTY = 0
    OBSTACLE = 1
    PIT = 2
    WUMPUS = 3
    GOLD = 4


    """
    Percept types
    """
    BUMP = OBSTACLE
    BREEZE = PIT
    STENCH = WUMPUS
    GLITTER = GOLD

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
        if self.cell_type == Cell.WUMPUS:
            self.cell_type = Cell.EMPTY
            return True
        return False

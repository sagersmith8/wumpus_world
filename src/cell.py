import cell_types


class Cell:
    def __init__(self, cell_type):
        """
        Constructs a cell of the given type

        :param cell_type: the type of the cell to construct
        :type cell_type: int
        :rtype: Cell
        :return: Cell of the given type
        """
        self.percepts = None
        self.cell_type = cell_type

    def get_percepts(self):
        return self.percepts

    def add_percept(self, percept):
        if self.percepts is None:
            self.percepts = set()

        if percept is not None:
            self.percepts.add(percept)

    def remove_percept(self, percept):
        self.percepts.discard(percept)

    def __str__(self):
        if self.cell_type == cell_types.WUMPUS:
            return '[W]'
        if self.cell_type == cell_types.EMPTY:
            return '[E]'
        if self.cell_type == cell_types.OBSTACLE:
            return '[O]'
        if self.cell_type == cell_types.GOLD:
            return '[G]'
        if self.cell_type == cell_types.PIT:
            return '[P]'

import cell_types


class Cell:
    def __init__(self, cell_type):
        """
        Constructs a cell of the given type, caching percepts.

        :param cell_type: the type of the cell to construct
        :type cell_type: int
        :rtype: Cell
        :return: Cell of the given type
        """
        self.percepts = None
        self.cell_type = cell_type

    def get_percepts(self):
        """
        Gets the percepts recorded for this cell.

        :rtype: set{int}
        :return: the percepts for this cell
        """
        return self.percepts

    def add_percept(self, percept):
        """
        Adds a percept to the given cell, ignoring 'None' and making sure
        there is a percept set if it is not yet created.

        :param percept: the percept to record
        :type percept: int
        :returns: nothing
        """
        if self.percepts is None:
            self.percepts = set()

        if percept is not None:
            self.percepts.add(percept)

    def remove_percept(self, percept):
        """
        Removes a percept from a given cell (for when a cell is changed).

        :param percept: the percept to remove
        :type percept: int
        :returns: nothing
        """
        if self.percepts:
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

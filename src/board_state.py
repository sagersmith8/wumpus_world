import cell_types
import directions
import environment
import percepts


class BoardState:
    def __init__(self, board, pos, direction):
        """
        Creates a new board with state to keep track of the game as it
        is played

        :param board: the initial set of cells in the board
        :type board: list[list[Cell]]
        :param pos: the initial position of the agent, given as column
            then row order
        :type pos: list[int]
        :param direction: the initial direction of the agent
        :type direction: int
        """
        self.board = board
        self.pos = list(pos)
        self.direction = direction
        self.arrows = self.count_wumpuses()

    def show(self, logger=None):
        """
        Prints a human readable representation of the current board-
        state.
        """
        if logger:
            for row in self.board:
                logger.info(''.join(map(str, row)))
            logger.info('Position: {}'.format(self.pos))
            logger.info('Direction: {}'.format(
                directions.NAMES[self.direction]))
            logger.info('Arrows: {}'.format(self.arrows))

        else:
            for row in self.board:
                print ''.join(map(str, row))
            print 'Position: {}'.format(self.pos)
            print 'Direction: {}'.format(directions.NAMES[self.direction])
            print 'Arrows: {}'.format(self.arrows)

    def get_board_percepts(self):
        """
        Returns the percepts the agent percieves purely due to its
        positioning relative to cells on the board.
        """
        current_cell = self.cell_at(self.pos)

        if current_cell.get_percepts() is None:
            current_cell.add_percept(
                environment.ON_SPOT_BOARD_PERCEPTS.get(current_cell.cell_type)
            )
            for adj_cell in self.adj_cells(self.pos):
                current_cell.add_percept(
                    environment.ADJACENT_BOARD_PERCEPTS.get(adj_cell.cell_type)
                )

        return current_cell.get_percepts()

    def count_wumpuses(self):
        """
        Counts the number of wumpuses on the board.

        :rtype: int
        :returns: the number of wumpuses one the board
        """
        count = 0
        for row in self.board:
            for cell in row:
                if cell.cell_type == cell_types.WUMPUS:
                    count += 1
        return count

    def turn_right(self):
        """
        Turn the agent stored in the board state clockwise
        (or right, from the agent's perspective).

        :rtype: None
        :returns: Nothing, but changes the agent's direction
        """
        self.direction = (self.direction + 1) % len(directions.DIRECTIONS)

    def turn_left(self):
        """
        Turn the agent stored in the board state anti-clockwise
        (or left, from the agent's perspective).

        :rtype: None
        :returns: Nothing, but changes the agent's direction
        """
        self.direction = (self.direction - 1) % len(directions.DIRECTIONS)

    def kill_wumpus(self, wumpus_pos):
        """
        Update the board state for killing a wumpus a the given position.
        - Change the cell where the wumpus was to empty
        - Remove the stench from adjacent cells

        :param wumpus_pos: the position of the wumpus to kill
        :type wumpus_pos: list[int]
        """
        wumpus_cell = self.cell_at(wumpus_pos)
        wumpus_cell.cell_type = cell_types.EMPTY

        for adj_cell in self.adj_cells(wumpus_pos):
            adj_cell.remove_percept(percepts.STENCH)

    def adj_cells(self, pos):
        """
        Gives the cells adjacent to a given position.

        :param pos: the given position
        :type pos: list[int]
        :rtype: generator
        :returns: an iterator for the cells adjacent to the current position
        """
        return (self.cell_at(move(pos, direction))
                for direction in directions.DIRECTIONS
                if self.on_board(move(pos, direction)))

    def cell_at(self, pos):
        """
        Gives the cell at a given posiition.

        :param pos: the given position
        :type pos: list[int]
        :rtype: Cell
        :returns: the cell at the given position, or None if that position
            on the board
        """
        if not self.on_board(pos):
            return None

        col, row = pos
        return self.board[row][col]

    def on_board(self, pos):
        """
        Determine whether a position is on the board, according to the size
        of the board.

        :rtype: bool
        :returns: whether a position is a valid position on the board
        """
        col, row = pos
        return (
            row >= 0 and row < len(self.board) and
            col >= 0 and col < len(self.board[row])
        )


def move(pos, direction):
    """
    Calculate where something will end up if it moves forward
    from the given position, facing the given direction, ignoring
    the edges of the board and obstacles.

    :rtype: [int]
    :returns: a 2-length list indicating where the object would
        end up appearing on an infinite empty board after moving
    """
    movement_vector = directions.MOVEMENTS[direction]

    return [
        pos[i] + movement_vector[i] for i in xrange(len(pos))
    ]

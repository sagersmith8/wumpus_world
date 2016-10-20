from cell import CellType
import environment


class Direction:
    """
    Direction enumeration: all of the cardinal directions.
    Used to store which way the agent is facing.
    """
    DIRECTIONS = range(4)
    NORTH, EAST, SOUTH, WEST = DIRECTIONS

    """
    Mapping of directions to movement vectors.
    That is, a map determining how an agent's position
    changes depending on which way it is facing when
    it moves forward.
    """
    MOVEMENTS = {
        NORTH: [0, 1],
        SOUTH: [0, -1],
        EAST:  [1, 0],
        WEST:  [-1, 0]
    }


class BoardState:
    def __init__(self, board, pos, direction):
        self.board = board
        self.pos = list(pos)
        self.direction = direction
        self.arrows = self.count_wumpuses()

    def get_board_percepts(self):
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
                if cell.cell_type == CellType.WUMPUS:
                    count += 1
        return count

    def turn_right(self):
        """
        Turn the agent stored in the board state clockwise
        (or right, from the agent's perspective).

        :rtype: None
        :returns: Nothing, but changes the agent's direction
        """
        self.direction = (self.direction + 1) % len(Direction.DIRECTIONS)

    def turn_left(self):
        """
        Turn the agent stored in the board state anti-clockwise
        (or left, from the agent's perspective).

        :rtype: None
        :returns: Nothing, but changes the agent's direction
        """
        self.direction = (self.direction - 1) % len(Direction.DIRECTIONS)

    def kill_wumpus(self, wumpus_pos):
        """
        Update the board state for killing a wumpus a the given position.
        - Change the cell where the wumpus was to empty
        - Remove the stench from adjacent cells
        """
        wumpus_cell = self.cell_at(wumpus_pos)
        wumpus_cell.cell_type = CellType.EMPTY

        for adj_cell in self.adj_cells(wumpus_pos):
            adj_cell.remove_percept(environment.STENCH)

    def adj_cells(self, pos):
        return (self.cell_at(move(pos, direction))
                for direction in Direction.DIRECTIONS
                if self.on_board(move(pos, direction)))

    def cell_at(self, pos):
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
    movement_vector = Direction.MOVEMENTS[direction]

    return [
        pos[i] + movement_vector[i] for i in xrange(len(pos))
    ]

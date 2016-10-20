from cell import CellType


class Percept:
    """
    Percepts consist of two types:
    - Board percepts; that is, percepts that persist if the agent
      stays in a particular board state.
      These percepts are BREEZE, STENCH, and GLITTER
    - Action percepts; that is, percepts that are only sensed
      immediately after performing an action.
      These percepts are BUMP and SCREAM
    """
    PERCEPTS = range(5)
    BREEZE, STENCH, GLITTER, BUMP, SCREAM = PERCEPTS


class Action:
    ACTIONS = range(5)
    LEFT, RIGHT, FORWARD, SHOOT, GRAB = ACTIONS

ADJACENT_BOARD_PERCEPTS = {
    CellType.PIT: Percept.BREEZE,
    CellType.WUMPUS: Percept.STENCH
}
ON_SPOT_BOARD_PERCEPTS = {
    CellType.GOLD: Percept.GLITTER
}

ACTION_NAME = {
    Action.LEFT:    'turn left',
    Action.RIGHT:   'turn right',
    Action.FORWARD: 'move forward',
    Action.SHOOT:   'shoot arrow',
    Action.GRAB:    'grab item'
}

ACTION_PENALTY = {
    Action.LEFT:    1,
    Action.RIGHT:   1,
    Action.FORWARD: 1,
    Action.SHOOT:   10,
    Action.GRAB:    1
}

DEATH_PENALTY = 1000
WUMPUS_KILL_REWARD = 10
GOLD_REWARD = 2000


class Environment:
    def __init__(self, board_state):
        self.board_state = board_state
        self.score = 0
        self.turn = 0
        self.action_percepts = set()
        self.scores = [0]
        self.actions = []
        self.deaths = []
        self.kills = []
        self.action_counts = {action: 0 for action in Action.ACTIONS}

    def clear_action_percepts(self):
        """
        Clears the action percepts from the last action.

        :rtype: None
        :returns: Nothing, but clears any percepts made by the last action
        """
        self.action_percepts.clear()

    def is_finished(self):
        """
        Tells whether the agent has reached the goal state.
        That is, tells whether the agent has picked up the gold.

        :rtype: bool
        :returns: whether the agent has picked up the gold yet
        """
        return self.finished

    def get_percepts(self):
        """
        Gives the percepts that are currently available to to the agent.

        :rtype: {int}
        :returns: a set of senses
        """
        percepts = self.action_percepts.copy()
        percepts.update(self.board_state.get_board_percepts())

        return percepts

    def _record_action(self, action):
        self.clear_action_percepts()

        self.actions.append(action)
        self.action_counts[action] += 1

        self.score -= ACTION_PENALTY[action]

    def _update_turn(self, action):
        self.scores.append(self.score)
        self.turn += 1

    def _kill_agent(self, death_pos, cell_type):
        self.score -= DEATH_PENALTY
        self.deaths.append((self.turn, death_pos, cell_type))

    def _kill_wumpus(self, wumpus_pos):
        self.board_state.kill_wumpus(wumpus_pos)
        self.score += WUMPUS_KILL_REWARD
        self.kills.append((self.turn, wumpus_pos))
        self.action_percepts.add(Percept.SCREAM)

    def _do_turn_left(self):
        self.board_state.turn_left()

    def _do_turn_right(self):
        self.board_state.turn_right()

    def _do_shoot(self):
        if self.board_state.arrows > 0:
            self.board_state.arrows -= 1

            arrow_pos = self.board_state.pos
            arrow_direction = self.board_state.direction

            while (self.board_state.on_board(arrow_pos) and
                   not self.board_state.cell_at(arrow_pos).stops_arrow()):
                arrow_pos = self.board_state.move(arrow_pos, arrow_direction)

            if (self.board_state.on_board(arrow_pos) and
                    self.board_state.cell_at(
                        arrow_pos
                    ).cell_type == CellType.WUMPUS):
                self._kill_wumpus(arrow_pos)

    def _do_grab(self):
        current_cell = self.board_state.cell_at(self.board_state.pos)

        if current_cell.cell_type == CellType.GOLD:
            self.finished = True
            self.score += GOLD_REWARD

    def _do_move_forward(self):
        next_pos = self.board_state.move_from(
            self.board_state.pos,
            self.board_state.direction
        )

        if not self.board_state.on_board(next_pos):
            self.action_percepts.add(Percept.BUMP)
            return

        next_cell = self.board_state.cell_at(next_pos)
        if next_cell.cell_type == CellType.OBSTACLE:
            self.action_percepts.add(Percept.BUMP)
            return

        if deadly(next_cell):
            self._kill_agent(next_pos, next_cell.cell_type)
            return

        # The agent should be able to move forward, given that they
        # didn't bump into something or die
        self.board_state.pos = next_pos

    ACTION_METHOD = {
        Action.LEFT:    _do_turn_left,
        Action.RIGHT:   _do_turn_right,
        Action.FORWARD: _do_move_forward,
        Action.SHOOT:   _do_shoot,
        Action.GRAB:    _do_grab
    }

    def perform_action(self, action):
        self._record_action(action)
        Environment.ACTION_METHOD[action](self)
        self._update_turn(action)

    def perform_actions(self, actions):
        for action in actions:
            self.perform_action(action)

    def turn_left(self):
        self.perform_action(Action.LEFT)

    def turn_right(self):
        self.perform_action(Action.RIGHT)

    def move_forward(self):
        self.perform_action(Action.FORWARD)

    def shoot(self):
        self.perform_action(Action.SHOOT)

    def grab(self):
        self.perform_action(Action.GRAB)


KILL_AGENT_CELLS = {CellType.PIT, CellType.WUMPUS}
STOP_ARROW_CELLS = {CellType.OBSTACLE, CellType.WUMPUS}


def deadly(cell):
    """
    Checks if the given cell will kill an agent that walks into it.

    :param cell: the cell to check for deadliness
    :type cell: Cell
    :rtype: bool
    :returns: True only if an agent will die if they walk into this cell
    """
    return cell.cell_type in Environment.KILL_AGENT_CELLS


def stops_arrow(cell):
    """
    Checks if the given cell will stop an arrow that flies into it.
    :param cell: the cell to check for arrow stopping
    :type cell: Cell
    :rtype: bool
    :returns: whether or not an arrow can safely pass through this cell
    """
    return cell.cell_type in Environment.STOP_ARROW_CELLS

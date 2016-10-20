import actions
import cell_types
import percepts


ADJACENT_BOARD_PERCEPTS = {
    cell_types.PIT:    percepts.BREEZE,
    cell_types.WUMPUS: percepts.STENCH
}
ON_SPOT_BOARD_PERCEPTS = {
    cell_types.GOLD:   percepts.GLITTER
}

ACTION_NAME = {
    actions.LEFT:    'turn left',
    actions.RIGHT:   'turn right',
    actions.FORWARD: 'move forward',
    actions.SHOOT:   'shoot arrow',
    actions.GRAB:    'grab item'
}

ACTION_PENALTY = {
    actions.LEFT:    1,
    actions.RIGHT:   1,
    actions.FORWARD: 1,
    actions.SHOOT:   10,
    actions.GRAB:    1
}

DEATH_PENALTY = 1000
WUMPUS_KILL_REWARD = 10
GOLD_REWARD = 1000


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
        self.action_counts = {action: 0 for action in actions.ACTIONS}

    def _clear_action_percepts(self):
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
        self._clear_action_percepts()

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
        self.action_percepts.add(percepts.SCREAM)

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
                    ).cell_type == cell_types.WUMPUS):
                self._kill_wumpus(arrow_pos)

    def _do_grab(self):
        current_cell = self.board_state.cell_at(self.board_state.pos)

        if current_cell.cell_type == cell_types.GOLD:
            self.finished = True
            self.score += GOLD_REWARD

    def _do_move_forward(self):
        next_pos = self.board_state.move_from(
            self.board_state.pos,
            self.board_state.direction
        )

        if not self.board_state.on_board(next_pos):
            self.action_percepts.add(percepts.BUMP)
            return

        next_cell = self.board_state.cell_at(next_pos)
        if next_cell.cell_type == cell_types.OBSTACLE:
            self.action_percepts.add(percepts.BUMP)
            return

        if deadly(next_cell):
            self._kill_agent(next_pos, next_cell.cell_type)
            return

        # The agent should be able to move forward, given that they
        # didn't bump into something or die
        self.board_state.pos = next_pos

    ACTION_METHOD = {
        actions.LEFT:    _do_turn_left,
        actions.RIGHT:   _do_turn_right,
        actions.FORWARD: _do_move_forward,
        actions.SHOOT:   _do_shoot,
        actions.GRAB:    _do_grab
    }

    def perform_action(self, action):
        self._record_action(action)
        Environment.ACTION_METHOD[action](self)
        self._update_turn(action)

    def perform_actions(self, actions):
        for action in actions:
            self.perform_action(action)

    def turn_left(self):
        self.perform_action(actions.LEFT)

    def turn_right(self):
        self.perform_action(actions.RIGHT)

    def move_forward(self):
        self.perform_action(actions.FORWARD)

    def shoot(self):
        self.perform_action(actions.SHOOT)

    def grab(self):
        self.perform_action(actions.GRAB)


KILL_AGENT_CELLS = {cell_types.PIT, cell_types.WUMPUS}
STOP_ARROW_CELLS = {cell_types.OBSTACLE, cell_types.WUMPUS}


def deadly(cell):
    """
    Checks if the given cell will kill an agent that walks into it.

    :param cell: the cell to check for deadliness
    :type cell: Cell
    :rtype: bool
    :returns: True only if an agent will die if they walk into this cell
    """
    return cell.cell_type in KILL_AGENT_CELLS


def stops_arrow(cell):
    """
    Checks if the given cell will stop an arrow that flies into it.
    :param cell: the cell to check for arrow stopping
    :type cell: Cell
    :rtype: bool
    :returns: whether or not an arrow can safely pass through this cell
    """
    return cell.cell_type in STOP_ARROW_CELLS

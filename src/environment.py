import actions
import cell_types
import percepts
import board_state as state

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
        """
        Constructs a new environment from an initial board state.
        """
        self.board_state = board_state
        self.score = 0
        self.turn = 0
        self.action_percepts = set()
        self.scores = [0]
        self.actions = []
        self.deaths = []
        self.kills = []
        self.finished = False
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

    def named_percepts(self):
        """
        Gives a named list of senses currently available to the agent.

        :rtype: list[string]
        :returns: a list of sense as strings
        """
        return map(
            lambda p: percepts.NAMES[p],
            self.get_percepts()
        )

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
        """
        Prepares for an action to be performed by adjusting the score,
        recording the action to be performed, and clearing the action
        percepts.

        :param action: the action that will be performed
        :type action: int
        """
        self._clear_action_percepts()

        self.actions.append(action)
        self.action_counts[action] += 1

        self.score -= ACTION_PENALTY[action]

    def _update_turn(self, action):
        """
        Cleans up after an action was performed by indexing the term
        number and recording the resulting score.

        :param action: the action that was performed
        :type action: int
        """
        self.scores.append(self.score)
        self.turn += 1

    def _kill_agent(self, death_pos, cell_type):
        """
        Processes the agent's death by updating their score with a
        death penalty, giving the agent a death percept, and
        recording the death.

        :param death_pos: where the agent died
        :type death_pos: list[int]
        :param cell_type: the type of cell the agent died in
        :type cell_type: int
        """
        self.score -= DEATH_PENALTY
        self.deaths.append((self.turn, death_pos, cell_type))
        self.action_percepts.add(percepts.DEATH)

    def _kill_wumpus(self, wumpus_pos):
        """
        Processses a wumpus' death by removing it from the board,
        rewarding the explorer the cost of shooting the arrow,
        recording the wumpus kill, and giving the agent a scream
        percept.

        :param wumpus_pos: where the wumpus died
        :type wumpus_pos: list[int]
        """
        self.board_state.kill_wumpus(wumpus_pos)
        self.score += WUMPUS_KILL_REWARD
        self.kills.append((self.turn, wumpus_pos))
        self.action_percepts.add(percepts.SCREAM)

    def _do_turn_left(self):
        """
        Changes the position of agent in the board_state to be
        facing left of its current direction.
        """
        self.board_state.turn_left()

    def _do_turn_right(self):
        """
        Changes the position of agent in the board_state to be
        facing right of its current direction.
        """
        self.board_state.turn_right()

    def _do_shoot(self):
        """
        Fires an arrow in the direction the agent is facing.
        If there is no obstacle in the way, kills the first
        wumpus the arrow would land on.
        """
        if self.board_state.arrows > 0:
            self.board_state.arrows -= 1

            arrow_pos = self.board_state.pos
            arrow_direction = self.board_state.direction

            while (self.board_state.on_board(arrow_pos) and
                   not stops_arrow(self.board_state.cell_at(arrow_pos))):
                arrow_pos = state.move(arrow_pos, arrow_direction)

            if (self.board_state.on_board(arrow_pos) and
                    self.board_state.cell_at(
                        arrow_pos
                    ).cell_type == cell_types.WUMPUS):
                self._kill_wumpus(arrow_pos)

    def _do_grab(self):
        """
        If the agent is over the gold, grabs the gold and wins the game,
        giving the explorer the reward. Otherwise, does nothing.
        """
        current_cell = self.board_state.cell_at(self.board_state.pos)

        if current_cell.cell_type == cell_types.GOLD:
            self.finished = True
            self.score += GOLD_REWARD

    def _do_move_forward(self):
        """
        Tries to move the agent forward one square, possibly killing
        or bumping the agent back in the process.
        """
        next_pos = state.move(
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
        """
        Performs a specified action, keeping track of move history,
        and other statistics.
        """
        self._record_action(action)
        Environment.ACTION_METHOD[action](self)
        self._update_turn(action)

    def perform_actions(self, actions):
        """
        Performs a list of actions, ignoring percepts and keeping
        track of statistics as they are performed.
        """
        for action in actions:
            self.perform_action(action)

    def turn_left(self):
        """
        Changes the agent's direction to be turned one direction anti-
        clockwise.
        """
        self.perform_action(actions.LEFT)

    def turn_right(self):
        """
        Changes the agent's direction to be turned one direction clockwise.
        """
        self.perform_action(actions.RIGHT)

    def move_forward(self):
        """
        Changes the agent's position to be moved forward one unit in the
        direction the agent was facing.

        An agent stays in the same place if:
        -the spot where the agent would move would kill them (and senses DEATH)
        -the spot where the agent would move has an obstacle (and senses BUMP)
        -the spot where the agent would move is off of the board
         (and senses BUMP)
        """
        self.perform_action(actions.FORWARD)

    def shoot(self):
        """
        Causes the agent to fire an arrow in the direction they are facing.
        """
        self.perform_action(actions.SHOOT)

    def grab(self):
        """
        Causes the agent to try to grab an item in the square they are
        currently located at. If there is gold in that square, the agent wins.
        """
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


def new_game(size):
    """
    Generate a new initial board state and environment of the given size.

    :param size: the size of the board to make
    :type size: int
    :rtype: tuple(BoardState, Environment)
    :returns: the board_state and corresponding environment for a new game
    """
    import generate_world

    world = generate_world.generate_world(size, 0.1, 0.1, 0.1)
    return world, Environment(world)


def see(env, logger=None):
    """
    Show the current board_state and the precepts from the environment

    :rtype: None
    :returns: Nothing, but prints the current state to the terminal
    """
    env.board_state.show(logger)
    if logger:
        logger.info('Percepts: %s', env.named_percepts())
    else:
        print "Percepts:", env.named_percepts()

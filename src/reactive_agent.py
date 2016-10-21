import actions
import directions
import percepts
from board_state import move
from navigation import Navigator


def adjacent(pos):
    """
    returns positions adjacent to a specified position

    :param pos: x, y coordinate of desired square
    :ptype: tuple(int, int)
    :rtype: list(tuple(int, int))
    :returns: list of positions adjacent to specified position
    """
    return {
        tuple(pos[i] + vec[i]
              for i in xrange(len(pos)))
        for vec in directions.MOVEMENTS.itervalues()
    }


def action_result(pos, dir, action):
    """
    returns result of a given action
    at a given positon, with a given direction

    :param pos: x, y coordinates before actions
    :ptype: tuple(int, int)
    :param dir: direction before action
    :ptype: int
    :param action: action taken
    :ptype: int
    :rtype: tuple(int, int), int
    :returns: result of a given action
        at a given positon, with a given direction
    """
    if action == actions.LEFT:
        return pos, (dir - 1) % 4
    if action == actions.RIGHT:
        return pos, (dir + 1) % 4
    else:
        return move(pos, dir), dir


def run(env, logger):
    """
    runs a reactive agent on a given environment, using the specified logger

    :param env: envirnoment in which the agent acts
    :ptype: environment
    :param logger: logger to be used for sample runs
    :ptype: logger
    """
    pos = (0, 0)
    dir = directions.NORTH
    dest_pos = [None]
    visited = set()
    safe = set()
    questionable = set()
    unsafe = set()
    actions_to_do = list()
    last_action = None

    def is_safe(pos):
        pos = tuple(pos)
        if pos in safe or pos in visited or pos == dest_pos[0]:
            return True
        return False

    navigator = Navigator(is_safe)

    while not env.is_finished():
        percept = env.get_percepts()
        logger.info("Percepts: %s", env.named_percepts())


        # update visited, safe, questionable, and unsafe
        if percepts.DEATH in percept or percepts.BUMP in percept:
            if last_action is not None:
                unnav_pos, dir = action_result(pos, dir, last_action)
            unsafe |= {tuple(unnav_pos)}
            logger.info("%s must be unnavigable", unnav_pos)
        else:
            if last_action is not None:
                pos, dir = action_result(pos, dir, last_action)
                pos = tuple(pos)
            visited |= {tuple(pos)}

            if percepts.BREEZE in percept or percepts.STENCH in percept:
                questionable |= (adjacent(pos) - (safe | visited | unsafe))
            else:
                logger.info("Due to lack of danger %s must be safe",
                            adjacent(pos) - (visited | unsafe))
                safe |= (adjacent(pos) - (visited | unsafe))

        if not actions_to_do:
            if percepts.GLITTER in percept:
                logger.info("Found gold, terminating...")
                env.grab()
            elif safe:
                dest_pos[0] = dest = safe.pop()
                logger.info("Starting navigation to safe square: %s", dest)
                actions_to_do = navigator.path_to(pos + (dir,), dest)
            elif questionable:
                dest_pos[0] = dest = questionable.pop()
                logger.info(
                    "Starting navigation to questionable square: %s", dest
                )
                actions_to_do = navigator.path_to(pos + (dir,), dest)
            else:
                logger.info("No squares left to go to, terminating...")
                return
        if actions_to_do:
            last_action = actions_to_do.pop(0)
            if last_action == actions.FORWARD:
                env.move_forward()
                logger.info("\tMoved Forward")
            elif last_action == actions.LEFT:
                env.turn_left()
                logger.info("\tTurned Left")
            elif last_action == actions.RIGHT:
                env.turn_right()
                logger.info("\tTurned Right")
            else:
                print(last_action)
            if len(actions_to_do) == 0:
                logger.info("Navigation ended")

if __name__ == '__main__':
    import environment
    import logging
    world, env = environment.new_game(10)

    logger = logging.getLogger('reactive_agent')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('reactive_agent_test_run.out')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    logger.info("---Initial State---")
    environment.see(env, logger)
    logger.info('')
    logger.info('---Reactive Agent Run---')
    run(env, logger)
    logger.info('')
    logger.info('Final Score: %s', env.score)

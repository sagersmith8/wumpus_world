import percepts
import navigation
import directions
import actions
from board_state import move

def adjacent(pos):
    return {tuple(pos[i] + vec[i] for i in xrange(len(pos))) for vec in directions.MOVEMENTS.itervalues()}

def action_result(pos, dir, action):
    if action == actions.LEFT:
        return pos, (dir - 1) % 4
    if action == actions.RIGHT:
        return pos, (dir + 1) % 4
    else:
        return move(pos, dir), dir


def run(env, logger):
    pos = (0, 0)
    dir = directions.NORTH
    visited = set()
    safe = set()
    questionable = set()
    unsafe = set()
    actions_to_do = list()
    def is_safe(x, y):
        if (x, y) in safe or (x, y) in visited:
            return True
        return False

    navigator = navigation(is_safe)

    while not env.is_finished():
        percept = env.get_percepts()
        logger.info("Percepts: %s", env.named_percepts())
        
        #update visited, safe, questionable, and unsafe
        if percepts.DEATH in percept or percepts.BUMP in percept:
            unnav_pos = action_result(pos, dir, last_action)
            unsafe |= unnav_pos
            logger.info("%s must be unnavigable", unnav_pos)
        else:
            pos, dir = action_result(pos, dir, last_action)
            visited |= pos

            if percepts.BREEZE in percept or percepts.STENCH in percept:
                questionable |= (adjacent((x,y)) - (safe | visited | unsafe))
            else:
                logger.info("Due to lack of danger %s must be safe", adjacent(pos) - (visited | unsafe))
                safe |= (adjacent(pos) - (visited | unsafe))

        if not actions_to_do:
            if percepts.GLITTER in percept:
                env.grab()
            elif safe:
                dest = safe.pop()
                logger.info("Starting navigation to safe square: %s", dest)
                actions_to_do = navigator.path_to(pos + (dir,), dest)
            elif questionable:
                dest = questionable.pop()
                logger.info("Starting navigation to questionable square: %s", dest)                
                actions_to_do = navigator.path_to(pos + (dir,), dest)
            else:
                logger.info("No squares left to go to, terminating...")
                return
        else:
            last_action = actions_to_do.popleft()
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
    file_handler = logging.FileHandler('../reactive_agent_test_run.out')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    logger.info("---Initial State---")
    environment.see(env, logger)
    logger.info('')
    logger.info('---Reactive Agent Run---')
    run(env, logger)

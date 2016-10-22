import actions
import directions
import percepts
from board_state import move
from navigation import Navigator
from node import const, func, var
from reactive_agent import adjacent
from reasoning_system import ReasoningSystem, Clause


"""
Axioms in clause form for making inferences about
the wumpus world.
"""
AXIOMS = [
    Clause(
        [
            func('pit', [func('pos',
                 [var('x', 1), var('y')]
            )]),
            func('pit', [func('pos',
                 [var('x', -1), var('y')]
            )]),
            func('pit', [func('pos',
                 [var('x'), var('y', 1)]
            )]),
            func('pit', [func('pos',
                 [var('x'), var('y', -1)]
            )])
        ],
        [func('sense', [
            const('BREEZE'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )]
    ),
    Clause(
        [func('sense', [
            const('BREEZE'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('pit', [func('pos',
                 [var('x', 1), var('y')]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('BREEZE'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('pit', [func('pos',
                 [var('x', -1), var('y')]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('BREEZE'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('pit', [func('pos',
                 [var('x'), var('y', 1)]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('BREEZE'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('pit', [func('pos',
                 [var('x'), var('y', -1)]
            )])
        ]
    ),
    Clause(
        [
            func('wumpus', [func('pos',
                 [var('x', 1), var('y')]
            )]),
            func('wumpus', [func('pos',
                 [var('x', -1), var('y')]
            )]),
            func('wumpus', [func('pos',
                 [var('x'), var('y', 1)]
            )]),
            func('wumpus', [func('pos',
                 [var('x'), var('y', -1)]
            )])            
        ],
        [func('sense', [
            const('STENCH'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )]
    ),
    Clause(
        [func('sense', [
            const('STENCH'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('wumpus', [func('pos',
                 [var('x', 1), var('y')]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('STENCH'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('wumpus', [func('pos',
                 [var('x', -1), var('y')]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('STENCH'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('wumpus', [func('pos',
                 [var('x'), var('y', 1)]
            )])
        ]
    ),
    Clause(
        [func('sense', [
            const('STENCH'),
            func('pos',
                 [var('x'), var('y')]
            )]
        )],
        [
            func('wumpus', [func('pos',
                 [var('x'), var('y', -1)]
            )])
        ]
    ),
    Clause(
        [func('safe',
              [func('pos',
                   [var('x'), var('y')]
              )]
        )],
        [func('pit',
              [func('pos',
                   [var('x'), var('y')]
              )]
        ),
        func('obstacle',
             [func('pos',
                  [var('x'), var('y')]
             )]
        ),
        func('wumpus',
             [func('pos',
                  [var('x'), var('y')]
             )]
        )]
    ),
    Clause(
        [],
        [func('safe',
              [func('pos',
                    [var('x'), var('y')]
              )]
        ),        
        func('wumpus',
             [func('pos',
                  [var('x'), var('y')]
             )]
        )]
    ),
    Clause(
        [],
        [func('safe',
              [func('pos',
                    [var('x'), var('y')]
              )]
        ),        
        func('pit',
             [func('pos',
                  [var('x'), var('y')]
             )]
        )]
    )
]


def action_result(pos, dire, action):
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
        return pos, (dire - 1) % 4
    if action == actions.RIGHT:
        return pos, (dire + 1) % 4
    if action == actions.FORWARD:
        return tuple(move(pos, dire)), dire
    return pos, dire


def position(cell):
    """
    Gives the function for a given position.

    :param cell: the position to represent
    :type cell: list[int]
    :rtype: Node
    :returns: a node representing that position
    """
    return func('pos', [
        const(coord) for coord in cell
    ])


def safe(cell):
    """
    Prodcues the clause to ask whether a cell is safe.

    :param cell: the cell to check
    :type cell: list[int]
    :rtype: Clause
    :returns: a clause to ask a ReasoningSystem if it
        can determine whether a cell is safe.
    """
    return Clause([func('safe', [position(cell)])], [])


def not_safe(cell):
    """
    Prodcues the clause to ask whether a cell is not safe.

    :param cell: the cell to check
    :type cell: list[int]
    :rtype: Clause
    :returns: a clause to ask a ReasoningSystem if it
        can determine whether a cell is not safe.
    """    
    return Clause([], [func('safe', [position(cell)])])


def wumpus(cell):
    """
    Prodcues the clause to ask whether a cell has a 
    wumpus.

    :param cell: the cell to check
    :type cell: list[int]
    :rtype: Clause
    :returns: a clause to ask a ReasoningSystem if it
        can determine whether a cell has a wumpus.
    """    
    return Clause([func('wumpus', [position(cell)])], [])


def not_wumpus(cell):
    """
    Prodcues the clause to ask whether a cell is not a
    wumpus.

    :param cell: the cell to check
    :type cell: list[int]
    :rtype: Clause
    :returns: a clause to ask a ReasoningSystem if it
        can determine whether a cell is not a wumpus.
    """    
    return Clause([], [func('wumpus', [position(cell)])])


def run(env, logger):
    """
    runs a reasoning agent on a given environment,
    using the specified logger

    :param env: envirnoment in which the agent acts
    :ptype: environment
    :param logger: logger to be used for sample runs
    :ptype: logger
    """    
    path_actions = []
    reasoner = ReasoningSystem(AXIOMS)
    current_pos = (0, 0)
    current_direction = directions.NORTH
    visited = set()
    unnavigable = set()
    safe_frontier = set()
    maybe_safe_frontier = set()
    wumpus_frontier = set()
    maybe_wumpus_frontier = set()        
    frontier = set()
    to_visit_frontier = [None]
    last_action = None

    def is_safe(pos):
        pos = tuple(pos)
        return pos in visited or pos == to_visit_frontier[0]

    navigator = Navigator(is_safe)
    
    while not env.is_finished():
        senses = env.get_percepts()
        logger.info("Percepts: %s", env.named_percepts())

        current_pos, current_direction = action_result(
            current_pos, current_direction, last_action
        )

        visited.add(current_pos)
        frontier |= (adjacent(current_pos) - visited)
        frontier -= visited
        frontier -= unnavigable

        if len(path_actions) > 0:
            last_action = path_actions.pop(0)
            env.perform_action(last_action)

            if len(path_actions) == 0:
                logger.info("Navigation ended")
            continue
        
        for percept in percepts.PERCEPTS:
            sense_node = func('sense', [
                const(percepts.NAMES[percept]),
                position(current_pos)
            ])
            if percept in senses:
                reasoner.tell(Clause([sense_node], []))
            else:
                reasoner.tell(Clause([], [sense_node]))

        if percepts.GLITTER in senses:
            logger.info("Found gold, terminating...")
            env.grab()
            continue          

        if percepts.BUMP in senses:
            logger.info("%s must be unnavigable due to BUMP", to_visit_frontier[0])
            frontier.discard(to_visit_frontier[0])
            unnavigable.add(to_visit_frontier[0])

        safe_frontier &= frontier
        safe_frontier |= {
            cell for cell in frontier - safe_frontier
            if reasoner.ask(safe(cell))
        }

        if safe_frontier:
            to_visit_frontier[0] = safe_frontier.pop()
            path_actions = navigator.path_to(
                current_pos + (current_direction,), to_visit_frontier[0]
            )
            logger.info(
                "Starting navigation to safe square: %s",
                to_visit_frontier[0]
            )

            last_action = path_actions.pop(0)
            env.perform_action(last_action)
            continue

        
        wumpus_frontier &= frontier
        wumpus_frontier |= {
            cell for cell in frontier - wumpus_frontier
            if reasoner.ask(wumpus(cell))
        }

        if wumpus_frontier:
            to_visit_frontier[0] = (visited & adjacent(wumpus_frontier.pop())).pop()
            path_actions = navigator.path_to(
                current_pos + (current_direction,), to_visit_frontier[0]
            )
            path_actions.append(actions.shoot)            
            logger.info(
                "Starting navigation to kill wumpus: %s",
                to_visit_frontier[0]
            )
            last_action = path_actions.pop(0)
            env.perform_action(last_action)
            continue


        maybe_wumpus_frontier &= frontier
        maybe_wumpus_frontier |= {
            cell for cell in frontier - maybe_wumpus_frontier
            if not reasoner.ask(not_wumpus(cell))
        }

        if maybe_wumpus_frontier:
            to_visit_frontier[0] = (visited &
                                 adjacent(maybe_wumpus_frontier.pop())).pop()
            path_actions = navigator.path_to(
                current_pos + (current_direction,), to_visit_frontier[0]
            )
            path_actions.append(actions.shoot)
            logger.info(
                "Starting navigation to kill wumpus: %s",
                to_visit_frontier[0]
            )
            last_action = path_actions.pop(0)
            env.perform_action(last_action)
            continue

        
        maybe_safe_frontier &= frontier
        maybe_safe_frontier |= {
            cell for cell in frontier - maybe_safe_frontier
            if not reasoner.ask(not_safe(cell))
        }
        
        if maybe_safe_frontier:
            to_visit_frontier[0] = maybe_safe_frontier.pop()
            path_actions = navigator.path_to(
                current_pos + (current_direction,), to_visit_frontier[0]
            )
            logger.info(
                "Starting navigation to questionable square: %s",
                to_visit_frontier[0]
            )
            last_action = path_actions.pop(0)
            env.perform_action(last_action)
            continue

        logger.info('No more squares to check, terminating...')
        return

if __name__ == '__main__':
    import environment
    import logging
    import sys

    sys.setrecursionlimit(200)
    
    world, env = environment.new_game(10)

    logger = logging.getLogger('reasoning_agent')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('reasoning_agent_test_run.out')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    logger.info("---Initial State---")
    environment.see(env, logger)
    logger.info('')
    logger.info('---Reasoning Agent Run---')
    run(env, logger)
    logger.info('')
    logger.info('Final Score: %s', env.score)
    

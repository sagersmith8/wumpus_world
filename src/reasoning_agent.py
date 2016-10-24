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
    Clause( # Determine that a square with a pit
        [   # is not safe, and a safe square is not a pit
        ],  # not(pit(pos(x, y))) or not(safe(pos(x, y)))
        [
            func('pit', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('safe', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),
    Clause( # Determine that a square with a wumpus
        [   # is not safe, and a safe square is not a wumpus
        ],
        [
            func('wumpus', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('safe', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),
    Clause( # Determine that an pit and a wumpus are different
        [   # that is, a pit is not a wumpus
        ],  # and a wumpus is not a pit
        [
            func('pit', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('wumpus', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),    
    Clause( # Determine that an empty square is safe
        [   # and an unsafe square is not empty
            func('safe', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('empty', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),
    Clause( # Determine that an obstacle square is safe
        [   # and an unsafe square is not an obstacle
            func('safe', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('obstacle', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),
    Clause( # Determine that an empty square and an obstacle are different
        [   # that is, an empty square is not an obstacle
        ],  # and an obstacle is not empty
        [
            func('empty', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('obstacle', [
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ]
    ),
    Clause( # Determine that the only unsafe squares are wumpuses or pits
        [   # That is, if something is unsafe and not a wumpus it must be a pit
            # And vice versa
            # Also, determine that non-pit, non-wumpus squares are safe
            func('safe', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('pit', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),
            func('wumpus', [
                func('pos', [
                    var('x'), var('y')
                ])
            ]),            
        ],
        [
        ]
    ),
    Clause( # Determine the location of a pit when there are three
        [   # non-pits next to a breeze
            func('pit', [
                func('pos', [
                    var('x', 1), var('y')
                ])
            ]),
            func('pit', [
                func('pos', [
                    var('x', -1), var('y')
                ])
            ]),
            func('pit', [
                func('pos', [
                    var('x'), var('y', 1)
                ])
            ]),
            func('pit', [
                func('pos', [
                    var('x'), var('y', -1)
                ])
            ])            
        ],
        [
            func('sense', [
                const('BREEZE'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])            
        ]
    ),
    Clause( # Determine the location of a wumpus when there are three 
        [   # non-wumpuses next to a stench
            func('wumpus', [
                func('pos', [
                    var('x', 1), var('y')
                ])
            ]),
            func('wumpus', [
                func('pos', [
                    var('x', -1), var('y')
                ])
            ]),
            func('wumpus', [
                func('pos', [
                    var('x'), var('y', 1)
                ])
            ]),
            func('wumpus', [
                func('pos', [
                    var('x'), var('y', -1)
                ])
            ])            
        ],
        [
            func('sense', [
                const('STENCH'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])            
        ]
    ),
    Clause( # infer a lack of pits from a lack of a breeze
        [   # on the right side
            func('sense', [
                const('BREEZE'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('pit', [
                func('pos', [
                    var('x', 1), var('y')
                ])
            ])
        ]
    ),
    Clause( # infer a lack of pits from a lack of a breeze
        [   # on the left side
            func('sense', [
                const('BREEZE'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('pit', [
                func('pos', [
                    var('x', -1), var('y')
                ])
            ])
        ]
    ),
    Clause( # infer a lack of pits from a lack of a breeze
        [   # on the upward side
            func('sense', [
                const('BREEZE'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('pit', [
                func('pos', [
                    var('x'), var('y', -1)
                ])
            ])
        ]
    ),
    Clause( # infer a lack of pits from a lack of a breeze
        [   # on the downward side
            func('sense', [
                const('BREEZE'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('pit', [
                func('pos', [
                    var('x'), var('y', 1)
                ])
            ])
        ]
    ),
    Clause( # infer a lack of wumpuses from a lack of a stench
        [   # on the right side
            func('sense', [
                const('STENCH'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('wumpus', [
                func('pos', [
                    var('x', 1), var('y')
                ])
            ])
        ]
    ),
    Clause( # infer a lack of wumpuses from a lack of a stench
        [   # on the left side
            func('sense', [
                const('STENCH'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('wumpus', [
                func('pos', [
                    var('x', -1), var('y')
                ])
            ])
        ]
    ),
    Clause( # infer a lack of wumpuses from a lack of a stench
        [   # on the upward side
            func('sense', [
                const('STENCH'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('wumpus', [
                func('pos', [
                    var('x'), var('y', -1)
                ])
            ])
        ]
    ),
    Clause( # infer a lack of wumpuses from a lack of a stench
        [   # on the downward side
            func('sense', [
                const('STENCH'),
                func('pos', [
                    var('x'), var('y')
                ])
            ])
        ],
        [
            func('wumpus', [
                func('pos', [
                    var('x'), var('y', 1)
                ])
            ])
        ]
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
        print "Current Percepts:", env.named_percepts()
        logger.info("Percepts: %s", env.named_percepts())

        if percepts.BUMP in senses or percepts.DEATH in senses:
            logger.info("%s must be unnavigable due to BUMP", to_visit_frontier[0])
            frontier.discard(to_visit_frontier[0])
            unnavigable.add(to_visit_frontier[0])
        else:
            current_pos, current_direction = action_result(
                current_pos, current_direction, last_action
            )
            visited.add(current_pos)
            reasoner.tell(safe(current_pos))

        frontier |= (adjacent(current_pos) - visited)
        frontier -= visited
        frontier -= unnavigable

        print "Current State:"
        plot_grid([visited, frontier, unnavigable],
                  ['V', 'F', 'U'],
                  current_pos,
                  current_direction
        )
        
        if len(path_actions) > 0:
            last_action = path_actions.pop(0)
            env.perform_action(last_action)

            if len(path_actions) == 0:
                logger.info("Navigation ended")
            continue
        
        for percept in [percepts.BREEZE, percepts.STENCH]:
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
            print "going from {} to {}".format(current_pos, to_visit_frontier[0])
            logger.info(
                "Starting navigation to safe square: %s",
                to_visit_frontier[0]
            )

            last_action = path_actions.pop(0)
            env.perform_action(last_action)
            continue

        print "No safe cell..."
        
        """wumpus_frontier &= frontier
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
            continue"""

        logger.info('No more squares to check, terminating...')
        return

def plot_grid(grid_list, grid_values, current_pos, current_dir):
    if all(len(grid_set) == 0 for grid_set in grid_list):
        print "Empty"
        return

    total_set = set()
    for grid_set in grid_list:
        total_set |= grid_set
    
    min_x = min(map(lambda c: c[0], total_set))
    max_x = max(map(lambda c: c[0], total_set))
    min_y = min(map(lambda c: c[1], total_set))
    max_y = max(map(lambda c: c[1], total_set))

    x_size = max_x - min_x + 1
    y_size = max_y - min_y + 1

    out_grid = [[[' ' for _ in xrange(len(grid_list) + 1)] for x in xrange(x_size)] for y in xrange(y_size)]

    for grid_num, grid_set in enumerate(grid_list):
        for x, y in grid_set:
            out_grid[y - min_y][x - min_x][grid_num] = grid_values[grid_num]

    cur_x, cur_y = current_pos
    out_grid[cur_y - min_y][cur_x - min_x][len(grid_list)] = directions.NAMES[current_dir][0]
            
    for num, row in enumerate(out_grid):
        print ''.join(map(lambda s: '[' + ''.join(s) + ']', row))
        
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
    

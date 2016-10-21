"""
Percept types:
-Action Percepts - percepts that appear for one turn and are the
                   result of an action.
 Percepts: BUMP and SCREAM
-Board Percepts - percepts that last as long as the board state
                  stays the same
 Percepts: GLITTER, BREEZE and STENCH
"""
PERCEPTS = range(6)
GLITTER, BREEZE, STENCH, BUMP, SCREAM, DEATH = PERCEPTS

NAMES = {
    GLITTER: 'GLITTER',
    BREEZE:  'BREEZE',
    STENCH:  'STENCH',
    BUMP:    'BUMP',
    SCREAM:  'SCREAM',
    DEATH:   'DEATH'
}

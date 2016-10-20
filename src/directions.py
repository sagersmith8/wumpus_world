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

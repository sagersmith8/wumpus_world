import directions
import actions


class Navigator:

    def __init__(self, reasoning_agent):
        self.reasoning_agent = reasoning_agent

    def path_to(self, cur_loc, final_loc):
        """
        Finds a path from the current location to the desired location

        :param cur_loc: position vector
        :type cur_loc: Tuple(int,int,int)
        :param final_loc: vector location of desired square
        :type final_loc: Tuple(int,int)
        :rtype: list[int]
        :return: queue of actions to take to get from the current square to the
            desired square
        """
        cur_x, cur_y, cur_dir = cur_loc
        fin_x, fin_y = final_loc

        return self.a_star(cur_x, cur_y, cur_dir, fin_x, fin_y)

    def a_star(self, cur_x, cur_y, cur_dir, fin_x, fin_y):
        """
        A start implementation for navigation

        :param cur_x: current column location of agent
        :type cur_x: int
        :param cur_y: current row location of agent
        :type cur_y: int
        :param cur_dir: cardinal direction agent is facing
        :type cur_dir: int
        :param fin_x: the desired column location of agent
        :type fin_x: int
        :param fin_y: the desired row location of agent
        :type fin_y: int
        :rtype: list[int]
        :return: A queue of actions to take to get from the current
            square to the desired square
        """
        frontier = list()
        frontier.append([cur_x, cur_y, cur_dir, []])
        came_from = dict()
        came_from[(cur_x, cur_y)] = None

        while len(frontier) > 0:
            x, y, direction, actions_to_take = frontier.pop(0)
            if (x, y) == (fin_x, fin_y):
                return actions_to_take

            to_visit = self.calculate_actions(
                x, y, direction, actions_to_take, self.get_neighbors(x, y)
            )

            to_visit.sort(key=lambda k: len(k[3]))
            for cell in to_visit:
                loc = (cell[0], cell[1])
                if loc not in came_from:
                    frontier.append(cell)
                    came_from[loc] = cell
        return None

    def get_neighbors(self, x, y):
        """
        Returns a list of safe cells to check

        :param x: x to get neighbors of
        :type x: int
        :param y: y to get neighbors of
        :type y: int
        :rtype: list[Tuple(int,int)]
        :return: list of places to check
        """
        return filter(
            self.reasoning_agent, [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
        )

    def calculate_next_direction_vec(self, loc, togo):
        """
        Calculates the direction to get to get to the desired
        square

        :param loc: your current location
        :type loc: tuple(int, int)
        :param togo: where you wanna go
        :type togo: tuple(int, int)
        :rtype: direction vector
        :return: The direction to the togo square
        """
        return [togo[0]-loc[0], togo[1]-loc[1]]

    def calculate_num_moves(self, direction_vec, next_direction_vec):
        """
        Calculates the number of moves needed to get to a square

        :param direction_vec: direction you are currently facing
        :type direction_vec: list[int, int]
        :param next_direction_vec: direction you want to go
        :type next_direction_vec: list[int, int]
        :rtype: int
        :return: number of moves to get to desired square
        """
        return max(
                abs(direction_vec[0]-next_direction_vec[0]),
                abs(direction_vec[1]-next_direction_vec[1])
            )

    def calculate_actions(self, x, y, direction, actions_to_take, to_visit):
        """
        Calculates the actions needed to get to the squares to to_visit

        :param x: current column
        :type x: int
        :param y: current row
        :type y: int
        :param direction: current direction
        :type direction: int
        :param actions_to_take: actions already taken
        :type actions_to_take: list[int]
        :param to_visit: squares to visit
        :type to_visit: list[[list[int,int]]
        :return: the actions needed to get to the desired squares
        """
        loc = [x, y]
        direction_vec = directions.MOVEMENTS[direction]
        for cell in to_visit:
            next_direction_vec = self.calculate_next_direction_vec(loc, cell)
            next_direction = directions.VECTORS[tuple(next_direction_vec)]
            num_moves = self.calculate_num_moves(
                direction_vec, next_direction_vec
            )
            cell.append(next_direction)
            cell.append(
                self.resolve_actions(
                    actions_to_take, direction,
                    next_direction, num_moves
                )
            )

        return to_visit

    def rotate(self, direction, next_direction):
        """
        Calculates which way to rotate to get to the desired direction
        :param direction: current direction
        :type direction: int
        :param next_direction: desired direction
        :type next_direction: int
        :rtype: int
        :return: action to take to get to desired direction
        """
        diff = abs(direction - next_direction)
        if diff == 0 or diff == 2:
            raise Exception()

        if diff == 1:
            return (
                actions.RIGHT
                if direction < next_direction
                else actions.LEFT
            )
        return actions.LEFT if direction < next_direction else actions.RIGHT

    def resolve_actions(
            self, actions_to_take, direction, next_direction, num_moves):
        """
        Returns the actions needed to get to the desired square

        :param actions_to_take: list to append
        :type actions_to_take: list[int]
        :param direction: direction you are facing
        :type direction: int
        :param next_direction: direction you want to go
        :type next_direction: int
        :param num_moves: number of moves required
        :type num_moves: int
        :rtype: list[int]
        :return: actions needed to get to desired square
        """
        if num_moves == 1:
            return (
                actions_to_take + [
                    self.rotate(direction, next_direction), actions.FORWARD
                ]
            )

        if num_moves == 0:
            return actions_to_take+[
                actions.FORWARD
            ]

        if num_moves == 2:
            return actions_to_take + [
                actions.LEFT,
                actions.LEFT,
                actions.FORWARD
            ]

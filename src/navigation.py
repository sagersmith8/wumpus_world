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
                print x, y
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
        return [togo[0]-loc[0], togo[1]-loc[1]]

    def calculate_num_moves(self, direction_vec, next_direction_vec):
        return max(
                abs(direction_vec[0]-next_direction_vec[0]),
                abs(direction_vec[1]-next_direction_vec[1])
            )

    def calculate_actions(self, x, y, direction, actions_to_take, to_visit):
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

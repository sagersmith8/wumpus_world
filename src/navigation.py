class Navigator:

    def __init__(self, board, reasoning_agent):
        self.board = board
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
        frontier.append((cur_x, cur_y))
        came_from = dict()
        came_from[(cur_x, cur_y)] = None

        while len(frontier) > 0:
            current = frontier.pop()
            if current == (fin_x, fin_y):
                break
            x, y = current
            to_visit = self.get_neighbors(x, y)
            for loc in to_visit:
                if loc not in came_from:
                    frontier.append(loc)
                    came_from[loc] = current
        return current

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
            self.reasoning_agent, [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        )

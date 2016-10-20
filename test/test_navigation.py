import unittest

from src.navigation import Navigator
from src.generate_world import generate_world
from src.cell_types import EMPTY


class TestNavigation(unittest.TestCase):
    def setUp(self):
        self.board, self.agent_loc = generate_world(5, 0, 0, 0)
        print self.agent_loc
        self.print_board()
        self.navigator = Navigator(
            self.board, self.fake_reasoning_agent
        )

    def test_simple_setup(self):
        final_loc = (0, 0)
        print self.navigator.path_to(self.agent_loc, final_loc)

    def fake_reasoning_agent(self, loc):
        return (
            0 <= loc[0] < len(self.board[0]) and
            0 <= loc[1] < len(self.board) and
            self.board[loc[1]][loc[0]].cell_type == EMPTY
        )

    def print_board(self):
        for row in self.board:
            cur_row = ''
            for cell in row:
                cur_row += str(cell)
            print cur_row

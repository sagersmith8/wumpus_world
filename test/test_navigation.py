import unittest

from src.navigation import Navigator
from src.generate_world import generate_world
from src.cell_types import EMPTY
from src.actions import LEFT, RIGHT, FORWARD
from src.directions import NORTH, SOUTH, EAST, WEST, MOVEMENTS


class TestNavigation(unittest.TestCase):
    def setUp(self):
        self.board_state = generate_world(5, 0, 0, 0)
        self.board = self.board_state.board
        self.agent_loc = (self.board_state.pos +
                          [self.board_state.direction])
        self.print_board()
        self.navigator = Navigator(
            self.fake_reasoning_agent
        )

    def test_simple_navigation_empty_board(self):
        final_loc = (0, 0)
        self.board_state.show()
        print self.navigator.path_to(self.agent_loc, final_loc)

    def fake_reasoning_agent(self, loc):
        return (
            0 <= loc[0] < len(self.board[0]) and
            0 <= loc[1] < len(self.board) and
            self.board[loc[1]][loc[0]].cell_type == EMPTY
        )

    def test_rotation_left(self):
        self.assertEqual(self.navigator.rotate(1, 0), LEFT)
        self.assertEqual(self.navigator.rotate(2, 1), LEFT)
        self.assertEqual(self.navigator.rotate(3, 2), LEFT)
        self.assertEqual(self.navigator.rotate(0, 3), LEFT)

    def test_rotation_right(self):
        self.assertEqual(self.navigator.rotate(0, 1), RIGHT)
        self.assertEqual(self.navigator.rotate(1, 2), RIGHT)
        self.assertEqual(self.navigator.rotate(2, 3), RIGHT)
        self.assertEqual(self.navigator.rotate(3, 0), RIGHT)

    def test_resolve_actions_same_dir(self):
        self.assertEqual(
            self.navigator.resolve_actions([], WEST, WEST, 0), [2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], NORTH, NORTH, 0), [2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], SOUTH, SOUTH, 0), [2])
        self.assertEqual(
            self.navigator.resolve_actions([], EAST, EAST, 0), [2]
        )

    def test_resolve_actions_dir_one_off(self):
        self.assertEqual(
            self.navigator.resolve_actions([], WEST, NORTH, 1), [RIGHT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], WEST, SOUTH, 1), [LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], NORTH, WEST, 1), [LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], NORTH, EAST, 1), [RIGHT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], EAST, NORTH, 1), [LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], EAST, SOUTH, 1), [RIGHT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], SOUTH, WEST, 1), [RIGHT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions([], SOUTH, EAST, 1), [LEFT, 2]
        )

    def test_resolve_actions_dir_opposites(self):
        self.assertEqual(
            self.navigator.resolve_actions(
                [], WEST, EAST, 2), [LEFT, LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions(
                [], NORTH, SOUTH, 2
            ), [LEFT, LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions(
                [], SOUTH, NORTH, 2
            ), [LEFT, LEFT, 2]
        )
        self.assertEqual(
            self.navigator.resolve_actions(
                [], EAST, WEST, 2), [LEFT, LEFT, 2]
        )

    def test_calculate_next_direction_vec(self):
        self.assertEqual(
            MOVEMENTS[NORTH],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[NORTH]
            )
        )
        self.assertEqual(
            MOVEMENTS[SOUTH],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[SOUTH]
            )
        )
        self.assertEqual(
            MOVEMENTS[EAST],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[EAST]
            )
        )
        self.assertEqual(
            MOVEMENTS[WEST],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[WEST]
            )
        )

    def test_calculate_num_moves_same(self):
        self.assertEqual(
            0, self.navigator.calculate_num_moves(
                MOVEMENTS[WEST], MOVEMENTS[WEST]
            )
        )
        self.assertEqual(
            0, self.navigator.calculate_num_moves(
                MOVEMENTS[EAST], MOVEMENTS[EAST]
            )
        )
        self.assertEqual(
            0, self.navigator.calculate_num_moves(
                MOVEMENTS[NORTH], MOVEMENTS[NORTH]
            )
        )
        self.assertEqual(
            0, self.navigator.calculate_num_moves(
                MOVEMENTS[SOUTH], MOVEMENTS[SOUTH]
            )
        )

    def test_calculate_num_moves_one_off(self):
        self.assertEqual(
            MOVEMENTS[WEST],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[WEST]
            )
        )

    def test_calculate_num_moves_opposites(self):
        self.assertEqual(
            MOVEMENTS[WEST],
            self.navigator.calculate_next_direction_vec(
                (0, 0), MOVEMENTS[WEST]
            )
        )

    def test_calculate_actions_north(self):
        to_visit = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1]]
        ]
        to_visit_expected_north = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1],
             NORTH, [FORWARD]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1],
             EAST, [RIGHT, FORWARD]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1], SOUTH,
             [LEFT, LEFT, FORWARD]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1], WEST,
             [LEFT, FORWARD]]
        ]

        self.assertEqual(
            self.navigator.calculate_actions(
                0, 0, NORTH, [], to_visit
            ),
            to_visit_expected_north
        )

    def test_calculate_actions_east(self):
        to_visit = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1]]
        ]
        to_visit_expected_east = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1],
             NORTH, [LEFT, FORWARD]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1],
             EAST, [FORWARD]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1],
             SOUTH, [RIGHT, FORWARD]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1],
             WEST, [LEFT, LEFT, FORWARD]]
        ]

        self.assertEqual(
            self.navigator.calculate_actions(
                0, 0, EAST, [], to_visit
            ),
            to_visit_expected_east
        )

    def test_calculate_actions_west(self):
        to_visit = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1]]
        ]
        to_visit_expected_west = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1],
             NORTH, [RIGHT, FORWARD]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1],
             EAST, [LEFT, LEFT, FORWARD]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1],
             SOUTH, [LEFT, FORWARD]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1],
             WEST, [FORWARD]]
        ]

        self.assertEqual(
            self.navigator.calculate_actions(
                0, 0, WEST, [], to_visit
            ),
            to_visit_expected_west
        )

    def test_calculate_actions_south(self):
        to_visit = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1]]
        ]
        to_visit_expected_south = [
            [MOVEMENTS[NORTH][0], MOVEMENTS[NORTH][1],
             NORTH, [LEFT, LEFT, FORWARD]],
            [MOVEMENTS[EAST][0], MOVEMENTS[EAST][1],
             EAST, [LEFT, FORWARD]],
            [MOVEMENTS[SOUTH][0], MOVEMENTS[SOUTH][1],
             SOUTH, [FORWARD]],
            [MOVEMENTS[WEST][0], MOVEMENTS[WEST][1],
             WEST, [RIGHT, FORWARD]]
        ]

        self.assertEqual(
            self.navigator.calculate_actions(
                0, 0, SOUTH, [], to_visit
            ),
            to_visit_expected_south
        )

    def print_board(self):
        for row in self.board:
            cur_row = ''
            for cell in row:
                cur_row += str(cell)
            print cur_row

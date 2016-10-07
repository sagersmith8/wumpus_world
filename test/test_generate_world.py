import unittest
import src.generate_world as generate_world
from src.cell import Cell


class TestGenerateWorld(unittest.TestCase):
    def test_generate_world_size_too_small(self):
        """
        Tests that a board is not created for a board that is too small
        """
        self.assertIsNone(generate_world.generate_world(4, 0, 0, 0))

    def test_generate_world_board_too_big(self):
        """
        Tests that a board is not created for a board that is too big
        """
        self.assertIsNone(generate_world.generate_world(26, 0, 0, 0))

    def test_generate_world_incorrect_probabilities(self):
        """
        Tests that a board is not created with incorrect probabilities
        """
        self.assertIsNone(generate_world.generate_world(5, 1, 1, 1))

    def test_generate_world_correct(self):
        """
        Tests that a board is created with correct input
        """
        board_size = 5
        board = generate_world.generate_world(board_size, .1, .1, .1)
        self.assertIsNotNone(board)
        self.assertEqual(board_size, len(board))
        empty_count = 0
        for row in board:
            self.assertEqual(board_size, len(row))
            for cell in row:
                self.assertIsNotNone(cell.cell_type)
                if cell.cell_type == Cell.EMPTY:
                    empty_count += 1
        self.assertGreaterEqual(empty_count, 2)


class TestCreateBoard(unittest.TestCase):
    def test_generate_board_correct(self):
        """
        Tests that a board is created with correct input
        """
        board_size = 5
        board = generate_world.create_board(board_size, .1, .1, .1)
        self.assertIsNotNone(board)
        self.assertEqual(board_size, len(board))
        empty_count = 0
        for row in board:
            self.assertEqual(board_size, len(row))
            for cell in row:
                self.assertIsNotNone(cell.cell_type)
                if cell.cell_type == Cell.EMPTY:
                    empty_count += 1
        self.assertGreaterEqual(empty_count, 2)


class TestCreateCell(unittest.TestCase):
    def test_create_cell(self):
        """
        Tests that a cell is created by create cell
        """
        cell = generate_world.create_cell(0, .2, 0)
        self.assertIsNotNone(cell)

    def test_probability(self):
        """
        Tests that the cell probability creation works correctly
        """
        empty_cells = [generate_world.create_cell(0, 0, 0) for _ in xrange(100)]
        obsical_cells = (
            [generate_world.create_cell(1, 0, 0) for _ in xrange(100)]
        )
        pit_cells = (
            [generate_world.create_cell(0, 1, 0) for _ in xrange(100)]
        )
        wumpus_cells = (
            [generate_world.create_cell(0, 0, 1) for _ in xrange(100)]
        )

        self.assertTrue(
            all(cell.cell_type == Cell.EMPTY for cell in empty_cells)
        )

        self.assertTrue(
            all(cell.cell_type == Cell.OBSTACLE for cell in obsical_cells)
        )

        self.assertTrue(
            all(cell.cell_type == Cell.PIT for cell in pit_cells)
        )

        self.assertTrue(
            all(cell.cell_type == Cell.WUMPUS for cell in wumpus_cells)
        )


class TestValidInput(unittest.TestCase):
    def test_valid_input_size_too_small(self):
        """
        Tests that input is not valid for a board that is too small
        """
        self.assertFalse(generate_world.valid_input(4, 0, 0, 0))

    def test_valid_too_big(self):
        """
        Tests that input is not for a board that is too big
        """
        self.assertFalse(generate_world.valid_input(26, 0, 0, 0))

    def test_valid_input_incorrect_probabilities(self):
        """
        Tests that input is invalid with incorrect probabilities
        """
        self.assertFalse(generate_world.valid_input(5, 1, 1, 1))

    def test_valid_input_correct(self):
        """
        Tests that valid input is valid
        """
        self.assertTrue(generate_world.valid_input(5, .1, .1, .1))


class TestCheckProb(unittest.TestCase):
    def test_board_too_small(self):
        """
        Tests that board that is too small doesn't work
        """
        self.assertFalse(generate_world.check_board_size(4))

    def test_board_too_big(self):
        """
        Tests that a board that is too big doesn't work
        """
        self.assertFalse(generate_world.check_board_size(26))

    def test_valid_board_size(self):
        """
        Tests that valid board size works
        """
        self.assertTrue(generate_world.check_board_size(5))


class CheckProb(unittest.TestCase):
    def test_check_prob_incorrect(self):
        """
        Test check probability of incorrect
        """
        self.assertFalse(generate_world.check_prob(1, 1, 1))

    def test_check_prob_correct(self):
        """
        Test check probability of correct
        """
        self.assertFalse(generate_world.check_prob(1, 0, 0))


class TestChooseEmptyCell(unittest.TestCase):
    def test_choose_empty_cell(self):
        """
        Test checks that an empty cell is chosen
        """
        empty_cells = [[0, 0]]
        self.assertEqual([0, 0], generate_world.choose_empty_cell(empty_cells))


class TestPlaceEmptyCell(unittest.TestCase):
    def test_place_in_empty_cell(self):
        """
        Test checks that the correct item is placed in an empty cell
        """
        empty_cells = [[0, 0]]
        board = [[Cell(Cell.EMPTY)]]
        generate_world.place_in_empty_cell(board, Cell.GOLD, empty_cells)
        self.assertEqual(Cell.GOLD, board[0][0].cell_type)

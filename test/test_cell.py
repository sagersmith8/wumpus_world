import unittest
from src.cell import Cell


class TestCell(unittest.TestCase):
    def test_empty_cell(self):
        """
        Tests that an empty cell can be created
        """
        cell = Cell(Cell.EMPTY)
        self.assertEqual(Cell.EMPTY, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_obstical_cell(self):
        """
        Tests that an obstical cell can be correctly created
        """
        cell = Cell(Cell.OBSTACLE)
        self.assertEqual(Cell.OBSTACLE, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_pit_cell(self):
        """
        Tests that a pit cell can be correctly created
        """
        cell = Cell(Cell.PIT)
        self.assertEqual(Cell.PIT, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_wumpus_cell(self):
        """
        Tests that a wumpus cell can be correctly created
        """
        cell = Cell(Cell.WUMPUS)
        self.assertEqual(Cell.WUMPUS, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_gold_cell(self):
        """
        Test that a gold cell can be correctly created
        """
        cell = Cell(Cell.GOLD)
        self.assertEqual(Cell.GOLD, cell.cell_type)
        self.assertIsNone(cell.percepts)

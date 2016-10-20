import unittest
from src.cell import Cell
from src import cell_types


class TestCell(unittest.TestCase):
    def test_empty_cell(self):
        """
        Tests that an empty cell can be created
        """
        cell = Cell(cell_types.EMPTY)
        self.assertEqual(cell_types.EMPTY, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_obstical_cell(self):
        """
        Tests that an obstical cell can be correctly created
        """
        cell = Cell(cell_types.OBSTACLE)
        self.assertEqual(cell_types.OBSTACLE, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_pit_cell(self):
        """
        Tests that a pit cell can be correctly created
        """
        cell = Cell(cell_types.PIT)
        self.assertEqual(cell_types.PIT, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_wumpus_cell(self):
        """
        Tests that a wumpus cell can be correctly created
        """
        cell = Cell(cell_types.WUMPUS)
        self.assertEqual(cell_types.WUMPUS, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_gold_cell(self):
        """
        Test that a gold cell can be correctly created
        """
        cell = Cell(cell_types.GOLD)
        self.assertEqual(cell_types.GOLD, cell.cell_type)
        self.assertIsNone(cell.percepts)

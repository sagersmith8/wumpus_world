import unittest
from src.cell import Cell, CellType


class TestCell(unittest.TestCase):
    def test_empty_cell(self):
        """
        Tests that an empty cell can be created
        """
        cell = Cell(CellType.EMPTY)
        self.assertEqual(CellType.EMPTY, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_obstical_cell(self):
        """
        Tests that an obstical cell can be correctly created
        """
        cell = Cell(CellType.OBSTACLE)
        self.assertEqual(CellType.OBSTACLE, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_pit_cell(self):
        """
        Tests that a pit cell can be correctly created
        """
        cell = Cell(CellType.PIT)
        self.assertEqual(CellType.PIT, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_wumpus_cell(self):
        """
        Tests that a wumpus cell can be correctly created
        """
        cell = Cell(CellType.WUMPUS)
        self.assertEqual(CellType.WUMPUS, cell.cell_type)
        self.assertIsNone(cell.percepts)

    def test_gold_cell(self):
        """
        Test that a gold cell can be correctly created
        """
        cell = Cell(CellType.GOLD)
        self.assertEqual(CellType.GOLD, cell.cell_type)
        self.assertIsNone(cell.percepts)

import unittest
from src.cell import Cell


class TestCell(unittest.TestCase):
    def test_empty_cell(self):
        """
        Tests that an empty cell can be created
        """
        cell = Cell(Cell.EMPTY)
        self.assertEqual(Cell.EMPTY, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_obstical_cell(self):
        """
        Tests that an obstical cell can be correctly created
        """
        cell = Cell(Cell.OBSTACLE)
        self.assertEqual(Cell.OBSTACLE, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_pit_cell(self):
        """
        Tests that a pit cell can be correctly created
        """
        cell = Cell(Cell.PIT)
        self.assertEqual(Cell.PIT, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_wumpus_cell(self):
        """
        Tests that a wumpus cell can be correctly created
        """
        cell = Cell(Cell.WUMPUS)
        self.assertEqual(Cell.WUMPUS, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_gold_cell(self):
        """
        Test that a gold cell can be correctly created
        """
        cell = Cell(Cell.GOLD)
        self.assertEqual(Cell.GOLD, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_kill_wumpus(self):
        """
        Tests that a wumpus is killed correctly
        """
        cell = Cell(Cell.WUMPUS)
        self.assertTrue(cell.kill())
        self.assertEqual(Cell.EMPTY, cell.cell_type)

    def test_not_kill_other_types(self):
        """
        Tests that only wumpus's can die
        """
        empty_cell = Cell(Cell.EMPTY)
        obstical_cell = Cell(Cell.OBSTACLE)
        pit_cell = Cell(Cell.PIT)
        gold_cell = Cell(Cell.GOLD)
        self.assertFalse(empty_cell.kill())
        self.assertFalse(obstical_cell.kill())
        self.assertFalse(pit_cell.kill())
        self.assertFalse(gold_cell.kill())
        self.assertNotEqual(Cell.EMPTY, obstical_cell.cell_type)
        self.assertNotEqual(Cell.EMPTY, pit_cell.cell_type)
        self.assertNotEqual(Cell.EMPTY, gold_cell.cell_type)

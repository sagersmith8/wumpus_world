import unittest
from src.cell_types import EMPTY, OBSTACLE, PIT, WUMPUS, GOLD
from src.cell import Cell


class TestCell(unittest.TestCase):
    def test_empty_cell(self):
        """
        Tests that an empty cell can be created
        """
        cell = Cell(EMPTY)
        self.assertEqual(EMPTY, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_obstical_cell(self):
        """
        Tests that an obstical cell can be correctly created
        """
        cell = Cell(OBSTACLE)
        self.assertEqual(OBSTACLE, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_pit_cell(self):
        """
        Tests that a pit cell can be correctly created
        """
        cell = Cell(PIT)
        self.assertEqual(PIT, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_wumpus_cell(self):
        """
        Tests that a wumpus cell can be correctly created
        """
        cell = Cell(WUMPUS)
        self.assertEqual(WUMPUS, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_gold_cell(self):
        """
        Test that a gold cell can be correctly created
        """
        cell = Cell(GOLD)
        self.assertEqual(GOLD, cell.cell_type)
        self.assertEqual(len(cell.percepts), 0)

    def test_kill_wumpus(self):
        """
        Tests that a wumpus is killed correctly
        """
        cell = Cell(WUMPUS)
        self.assertTrue(cell.kill())
        self.assertEqual(EMPTY, cell.cell_type)

    def test_not_kill_other_types(self):
        """
        Tests that only wumpus's can die
        """
        empty_cell = Cell(EMPTY)
        obstical_cell = Cell(OBSTACLE)
        pit_cell = Cell(PIT)
        gold_cell = Cell(GOLD)
        self.assertFalse(empty_cell.kill())
        self.assertFalse(obstical_cell.kill())
        self.assertFalse(pit_cell.kill())
        self.assertFalse(gold_cell.kill())
        self.assertNotEqual(EMPTY, obstical_cell.cell_type)
        self.assertNotEqual(EMPTY, pit_cell.cell_type)
        self.assertNotEqual(EMPTY, gold_cell.cell_type)

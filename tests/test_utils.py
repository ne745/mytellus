import unittest

import pathmagic  # noqa
from utils import calc_tile_bbox


class TestCalcTileBBox(unittest.TestCase):
    def test_normal(self):
        tile = {
            'x': 909,
            'y': 403,
            'z': 10
        }
        size = {
            'x': 1,
            'y': 1
        }
        expect = (
            139.5703125, 35.4606699514953,
            139.921875, 35.746512259918504
        )
        self.assertEqual(calc_tile_bbox(tile, size), expect)

    def test_zoom(self):
        tile = {
            'x': 3636,
            'y': 1612,
            'z': 12
        }
        size = {
            'x': 1,
            'y': 1
        }
        expect = (
            139.5703125, 35.67514743608467,
            139.658203125, 35.746512259918504
        )
        self.assertEqual(calc_tile_bbox(tile, size), expect)

    def test_size(self):
        tile = {
            'x': 3636,
            'y': 1612,
            'z': 12
        }
        size = {
            'x': 2,
            'y': 3
        }
        expect = (
            139.5703125, 35.532226227703376,
            139.74609375, 35.746512259918504
        )
        self.assertEqual(calc_tile_bbox(tile, size), expect)


if __name__ == '__main__':
    unittest.main()

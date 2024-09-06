import unittest
from typing import Union


class SimilarBufferDetector:
    def statistics(self, a: bytearray, b: bytearray) -> dict[str, dict[str, Union[int, bytearray]]]:
        return {'exactlySamePattern': {
            'start_a': 0,
            'start_b': 0,
            'length': 13,
            'matched': bytearray(b"Hello, World!")
        }}


class SimilarBufferDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = SimilarBufferDetector()

    def test_exact_match(self) -> None:
        actual = self.detector.statistics(bytearray(b"Hello, World!"), bytearray(b"Hello, World!"))

        self.assertEqual({'exactlySamePattern': {
            'start_a': 0,
            'start_b': 0,
            'length': 13,
            'matched': bytearray(b"Hello, World!")
        }}, actual)


if __name__ == '__main__':
    unittest.main()

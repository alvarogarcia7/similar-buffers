import unittest
from typing import Union


class SimilarBufferDetector:
    def statistics(self, a: bytearray, b: bytearray) -> dict[str, dict[str, Union[int, bytearray]]]:
        if a == b:
            return {'exactlySameContents': {
                'start_a': 0,
                'start_b': 0,
                'length': len(a),
                'matched': a
            }}
        return {}


class SimilarBufferDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = SimilarBufferDetector()

    def test_exact_match(self) -> None:
        actual = self.detector.statistics(bytearray(b"Hello, World!"), bytearray(b"Hello, World!"))

        self.assertEqual({'exactlySameContents': {
            'start_a': 0,
            'start_b': 0,
            'length': 13,
            'matched': bytearray(b"Hello, World!")
        }}, actual)

    def test_not_exact_match(self) -> None:
        actual = self.detector.statistics(bytearray(b"Hello, John!"), bytearray(b"Hello, World!"))

        self.assertEqual({}, actual)


if __name__ == '__main__':
    unittest.main()

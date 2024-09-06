import unittest

from similar_buffers import SimilarBufferDetector, ExactlySameContents, SameContents


class SimilarBufferDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = SimilarBufferDetector(ExactlySameContents(), SameContents())

    def test_exact_match(self) -> None:
        actual = self.detector.statistics(
            bytearray(b"Hello, World!"), bytearray(b"Hello, World!")
        )

        self.assertEqual(
            [
                {
                    "exactlySameContents": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 13,
                        "matched": bytearray(b"Hello, World!"),
                    }
                }
            ],
            actual,
        )

    def test_not_exact_match(self) -> None:
        actual = self.detector.statistics(
            bytearray(b"Hello, John!"), bytearray(b"Hello, World!")
        )

        self.assertEqual(
            [
                {
                    "sameContents": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": len(bytearray(b"Hello, ")),
                        "matched": bytearray(b"Hello, "),
                    }
                },
                {
                    "sameContents": {
                        "start_a": 8,
                        "start_b": 8,
                        "length": 1,
                        "matched": bytearray(b"o"),
                    }
                },
            ],
            actual,
        )


class ExactlySameContentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.statistic = ExactlySameContents()

    def test_exact_match(self) -> None:
        actual = self.statistic.detect(
            bytearray(b"Hello, World!"), bytearray(b"Hello, World!")
        )

        self.assertEqual(
            [
                {
                    "exactlySameContents": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 13,
                        "matched": bytearray(b"Hello, World!"),
                    }
                }
            ],
            actual,
        )

    def test_not_exact_match(self) -> None:
        actual = self.statistic.detect(
            bytearray(b"Hello, John!"), bytearray(b"Hello, World!")
        )

        self.assertEqual([], actual)


if __name__ == "__main__":
    unittest.main()

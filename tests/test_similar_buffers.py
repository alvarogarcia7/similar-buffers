import unittest
from unittest.mock import MagicMock

from similar_buffers import ExactlySameContents, SameContents
from similar_buffers import SimilarBufferDetector, Statistic


class SimilarBufferDetectorMockTest(unittest.TestCase):
    def test_all_statistics_executed(self) -> None:
        mock_statistic1 = MagicMock(spec=Statistic)
        mock_statistic2 = MagicMock(spec=Statistic)

        mock_statistic1.detect.return_value = []
        mock_statistic2.detect.return_value = []

        detector = SimilarBufferDetector(mock_statistic1, mock_statistic2)

        a = bytearray(b"Hello, World!")
        b = bytearray(b"Hello, World!")
        detector.statistics(a, b)

        mock_statistic1.detect.assert_called_once_with(a, b)
        mock_statistic2.detect.assert_called_once_with(a, b)


class SimilarBufferDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = SimilarBufferDetector(ExactlySameContents(), SameContents())

    def test_exact_match(self) -> None:
        actual = self.detector.statistics(
            bytearray(b"Hello, World!"), bytearray(b"Hello, World!")
        )

        self.assertEqual(
            [{"exactlySameContents": {}}],
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
                        "start": 0,
                        "length": len(bytearray(b"Hello, ")),
                        "matched": bytearray(b"Hello, "),
                    }
                },
                {
                    "sameContents": {
                        "start": 8,
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
            [{"exactlySameContents": {}}],
            actual,
        )

    def test_not_exact_match(self) -> None:
        actual = self.statistic.detect(
            bytearray(b"Hello, John!"), bytearray(b"Hello, World!")
        )

        self.assertEqual([], actual)


class SameContentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.statistic = SameContents()

    def test_no_match(self) -> None:
        actual = self.statistic.detect(
            bytearray(b"Hello, World!"), bytearray(b"Hello, World!")
        )

        self.assertEqual([], actual)

    def test_several_matches(self) -> None:
        actual = self.statistic.detect(
            bytearray(b"Hello, John!"), bytearray(b"Hello, World!")
        )

        self.assertEqual(
            [
                {
                    "sameContents": {
                        "start": 0,
                        "length": len(bytearray(b"Hello, ")),
                        "matched": bytearray(b"Hello, "),
                    }
                },
                {
                    "sameContents": {
                        "start": 8,
                        "length": 1,
                        "matched": bytearray(b"o"),
                    }
                },
            ],
            actual,
        )


if __name__ == "__main__":
    unittest.main()

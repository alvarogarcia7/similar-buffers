import unittest
from unittest.mock import MagicMock

from similar_buffers import ExactlySameContents, SameContents, SameContents2
from similar_buffers import SimilarBufferDetector, Statistic


class SimilarBufferDetectorMockTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.statistic1 = self.mock_statistic()
        self.statistic2 = self.mock_statistic()
        self.detector = SimilarBufferDetector(self.statistic1, self.statistic2)

    def test_all_statistics_executed(self) -> None:
        a = bytearray(b"Hello, World!")
        b = bytearray(b"Hello, World!")

        self.detector.statistics(a, b)

        self.statistic1.detect.assert_called_once_with(a, b)
        self.statistic2.detect.assert_called_once_with(a, b)

    @staticmethod
    def mock_statistic() -> MagicMock:
        mock_statistic1 = MagicMock(spec=Statistic)
        mock_statistic1.detect.return_value = []
        return mock_statistic1


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


class SameContents2Test(unittest.TestCase):
    def setUp(self) -> None:
        self.statistic = SameContents2()

    def test_no_match(self) -> None:
        actual = self.statistic.detect(bytearray(b"1234"), bytearray(b"5678"))

        self.assertEqual([], actual)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import MagicMock

from similar_buffers import ExactlySameContents, SameContents, SameStrings
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


class SameStringsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.statistic = SameStrings()

    def test_no_match(self) -> None:
        actual = self.statistic.detect(bytearray(b"1234"), bytearray(b"5678"))

        self.assertEqual([], actual)

    def test_no_match_when_integers(self) -> None:
        actual = self.statistic.detect(
            bytearray([i for i in range(0, 10)]), bytearray([i for i in range(10, 20)])
        )

        self.assertEqual([], actual)

    def test_no_match_when_empty_variables(self) -> None:
        actual = self.statistic.detect(bytearray(b""), bytearray(b""))

        self.assertEqual([], actual)

    def test_no_match_when_a_empty(self) -> None:
        actual = self.statistic.detect(bytearray(b""), bytearray(b"1"))

        self.assertEqual([], actual)

    def test_no_match_when_b_empty(self) -> None:
        actual = self.statistic.detect(bytearray(b"1"), bytearray(b""))

        self.assertEqual([], actual)

    def test_exact_match(self) -> None:
        actual = self.statistic.detect(bytearray(b"1234"), bytearray(b"1234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                }
            ],
            actual,
        )

    def test_in_the_middle(self) -> None:
        actual = self.statistic.detect(bytearray(b"0023400"), bytearray(b"1123411"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 2,
                        "start_b": 2,
                        "length": 3,
                        "matched": bytearray(b"234"),
                    }
                }
            ],
            actual,
        )

    def test_multiple_matches_multiple_chars(self) -> None:
        actual = self.statistic.detect(bytearray(b"00x234x11"), bytearray(b"00y234y11"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 2,
                        "matched": bytearray(b"00"),
                    }
                },
                {
                    "sameString": {
                        "start_a": 3,
                        "start_b": 3,
                        "length": 3,
                        "matched": bytearray(b"234"),
                    }
                },
                {
                    "sameString": {
                        "start_a": 7,
                        "start_b": 7,
                        "length": 2,
                        "matched": bytearray(b"11"),
                    }
                },
            ],
            actual,
        )

    def test_multiple_matches_multiple_chars_with_repeated_chars(self) -> None:
        """It detects the match from the beginning of a 00 with the end of b 00"""
        actual = self.statistic.detect(bytearray(b"00x234x00"), bytearray(b"00y234y00"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "length": 2,
                        "matched": bytearray(b"00"),
                        "start_a": 0,
                        "start_b": 0,
                    }
                },
                {
                    "sameString": {
                        "length": 1,
                        "matched": bytearray(b"0"),
                        "start_a": 7,
                        "start_b": 1,
                    }
                },
                {
                    "sameString": {
                        "length": 1,
                        "matched": bytearray(b"0"),
                        "start_a": 8,
                        "start_b": 1,
                    }
                },
                {
                    "sameString": {
                        "length": 3,
                        "matched": bytearray(b"234"),
                        "start_a": 3,
                        "start_b": 3,
                    }
                },
                {
                    "sameString": {
                        "length": 2,
                        "matched": bytearray(b"00"),
                        "start_a": 0,
                        "start_b": 7,
                    }
                },
                {
                    "sameString": {
                        "length": 1,
                        "matched": bytearray(b"0"),
                        "start_a": 7,
                        "start_b": 8,
                    }
                },
                {
                    "sameString": {
                        "length": 1,
                        "matched": bytearray(b"0"),
                        "start_a": 8,
                        "start_b": 8,
                    }
                },
            ],
            actual,
        )

    def test_partial_match_beginning_inverse(self) -> None:
        actual = self.statistic.detect(bytearray(b"123"), bytearray(b"1234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 3,
                        "matched": bytearray(b"123"),
                    }
                }
            ],
            actual,
        )

    def test_partial_match_end(self) -> None:
        actual = self.statistic.detect(bytearray(b"1234"), bytearray(b"234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 1,
                        "start_b": 0,
                        "length": 3,
                        "matched": bytearray(b"234"),
                    }
                }
            ],
            actual,
        )

    def test_partial_match_end_inverse(self) -> None:
        actual = self.statistic.detect(bytearray(b"234"), bytearray(b"1234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 1,
                        "length": 3,
                        "matched": bytearray(b"234"),
                    }
                }
            ],
            actual,
        )

    def test_multiple_matches(self) -> None:
        actual = self.statistic.detect(bytearray(b"12341234"), bytearray(b"1234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                },
                {
                    "sameString": {
                        "start_a": 4,
                        "start_b": 0,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                },
            ],
            actual,
        )

    def test_multiple_matches_inverse(self) -> None:
        actual = self.statistic.detect(bytearray(b"1234"), bytearray(b"12341234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                },
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 4,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                },
            ],
            actual,
        )

    def test_overlapping_matches(self) -> None:
        actual = self.statistic.detect(bytearray(b"1231234"), bytearray(b"1234"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 3,
                        "matched": bytearray(b"123"),
                    }
                },
                {
                    "sameString": {
                        "start_a": 3,
                        "start_b": 0,
                        "length": 4,
                        "matched": bytearray(b"1234"),
                    }
                },
            ],
            actual,
        )

    def test_single_character_match(self) -> None:
        actual = self.statistic.detect(bytearray(b"1"), bytearray(b"1"))
        self.assertEqual(
            [
                {
                    "sameString": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": 1,
                        "matched": bytearray(b"1"),
                    }
                }
            ],
            actual,
        )

    def test_case_sensitivity(self) -> None:
        actual = self.statistic.detect(bytearray(b"abc"), bytearray(b"ABC"))
        self.assertEqual([], actual)

    def test_empty_bytearrays(self) -> None:
        actual = self.statistic.detect(bytearray(b""), bytearray(b""))
        self.assertEqual([], actual)

    def test_large_bytearrays_multiple_matches(self) -> None:
        a = bytearray(b"1234" * 3)
        b = bytearray(b"1234")
        actual = self.statistic.detect(a, b)
        expected = [
            {
                "sameString": {
                    "start_a": i * 4,
                    "start_b": 0,
                    "length": 4,
                    "matched": bytearray(b"1234"),
                }
            }
            for i in range(3)
        ]
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

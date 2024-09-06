import unittest
from typing import Union


class SimilarBufferDetector:
    def statistics(
        self, a: bytearray, b: bytearray
    ) -> list[dict[str, dict[str, Union[int, bytearray]]]]:
        if a == b:
            return [
                {
                    "exactlySameContents": {
                        "start_a": 0,
                        "start_b": 0,
                        "length": len(a),
                        "matched": a,
                    }
                }
            ]

        matches = []
        current_match = []
        for i in range(len(a)):
            if a[i] == b[i]:
                current_match.append(i)
            else:
                if current_match:
                    matches.append(current_match)
                    current_match = []

        m = []
        for i in range(len(matches)):
            start_a = matches[i][0]
            start_b = matches[i][0]
            length = len(matches[i])
            matched = a[start_a : start_a + length]
            m.append(
                {
                    "sameContents": {
                        "start_a": start_a,
                        "start_b": start_b,
                        "length": length,
                        "matched": matched,
                    }
                }
            )
        return m  # type: ignore


class SimilarBufferDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = SimilarBufferDetector()

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


if __name__ == "__main__":
    unittest.main()

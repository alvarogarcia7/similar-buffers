import abc
from typing import Any


class Statistic:
    @abc.abstractmethod
    def detect(self, a: bytearray, b: bytearray) -> list[dict[str, Any]]:
        pass


class ExactlySameContents(Statistic):
    def detect(self, a: bytearray, b: bytearray) -> list[dict[str, Any]]:
        if a == b:
            return [{"exactlySameContents": {}}]
        return []


class SameContents(Statistic):
    def detect(self, a: bytearray, b: bytearray) -> list[dict[str, Any]]:
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
                        "start": start_a,
                        "length": length,
                        "matched": matched,
                    }
                }
            )
        return m  # type: ignore


class SimilarBufferDetector:
    def __init__(self, *statistics: Statistic) -> None:
        self._statistics = statistics

    def statistics(self, a: bytearray, b: bytearray) -> list[dict[str, Any]]:
        result = []
        for stat in self._statistics:
            result += stat.detect(a, b)
        return result


class SameStrings(Statistic):
    def detect(self, a: bytearray, b: bytearray) -> list[dict[str, Any]]:
        matches = []

        if len(a) > len(b):
            longest = a
            shortest = b
            longest_key = "a"
            shortest_key = "b"
        else:
            longest = b
            shortest = a
            longest_key = "b"
            shortest_key = "a"

        assert longest_key != shortest_key

        i = 0
        while i < len(longest):
            j = 0
            while j < len(shortest):
                if longest[i] == shortest[j]:
                    start_longest = i
                    start_shortest = j
                    length = 0
                    while (
                        i < len(longest)
                        and j < len(shortest)
                        and longest[i] == shortest[j]
                    ):
                        length += 1
                        i += 1
                        j += 1
                    matches.append(
                        {
                            "sameString": {
                                f"start_{longest_key}": start_longest,
                                f"start_{shortest_key}": start_shortest,
                                "length": length,
                                "matched": longest[
                                    start_longest : start_longest + length
                                ],
                            }
                        }
                    )
                    i -= 1
                    j -= 1
                j += 1
            i += 1

        return matches

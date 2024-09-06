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

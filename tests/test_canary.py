import unittest


class CanaryTest(unittest.TestCase):
    def test_everything_is_working(self) -> None:
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

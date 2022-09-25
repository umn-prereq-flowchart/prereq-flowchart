import unittest


class ExampleTest(unittest.TestCase):
    def test_two_plus_two(self) -> None:
        self.assertEqual(2 + 2, 4)

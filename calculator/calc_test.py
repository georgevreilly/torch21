import sys
import unittest

from calculator.calc import Calculator

print(f"{sys.path=}")

# Just to force a build and runtime dependency on Torch,
# though we don't use it (yet)
import torch  # type: ignore


class TestSum(unittest.TestCase):
    def test_sum(self):
        calculator = Calculator()
        self.assertEqual(calculator.add(1, 2), 3)


if __name__ == "__main__":
    unittest.main()

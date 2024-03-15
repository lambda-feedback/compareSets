import unittest

try:
    from .evaluation import Params, evaluation_function
except ImportError:
    from evaluation import Params, evaluation_function


class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_returns_is_correct_true_ascii(self):
        response, answer, params = "A n B", "A n B", Params()

        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A \\cap B")

    def test_returns_is_correct_true_latex(self):
        response, answer, params = "A \\cap B", "A n B", Params(is_latex=True)

        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), True)
        self.assertEqual(result.get("response_latex"), "A \\cap B")

    def test_returns_is_correct_false(self):
        response, answer, params = "A n B", "A u B", Params()

        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), False)
        self.assertEqual(result.get("response_latex"), "A \\cap B")

    def test_returns_is_correct_false_not_parseable(self):
        response, answer, params = "", "A u B", Params()

        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), False)
        self.assertEqual(result.get("response_latex"), None)

if __name__ == "__main__":
    unittest.main()

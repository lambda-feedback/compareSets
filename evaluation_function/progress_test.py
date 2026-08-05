import os
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock, patch

from .evaluation import Params, evaluation_function


def _wait_for_progress_executor():
    """Block until all currently-submitted background progress posts finish."""
    import lf_toolkit.evaluation.progress as progress_module

    progress_module._executor.shutdown(wait=True)
    progress_module._executor = ThreadPoolExecutor(
        max_workers=2, thread_name_prefix="lf-progress"
    )


class TestEvaluationFunctionProgress(unittest.TestCase):
    """
    Tests that evaluation_function() reports progress via lf_toolkit's
    report_progress() at the expected checkpoints, and stays a no-op when
    EVAL_PROGRESS_URL isn't set (the case for every other test in this repo).
    """

    def test_no_progress_reported_when_env_var_unset(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("EVAL_PROGRESS_URL", None)

            with patch("lf_toolkit.evaluation.progress.requests.post") as mock_post:
                evaluation_function("A n B", "A n B", Params())
                _wait_for_progress_executor()

        mock_post.assert_not_called()

    def test_reports_progress_at_parse_and_compare_checkpoints(self):
        with patch.dict(os.environ, {"EVAL_PROGRESS_URL": "http://127.0.0.1:9999"}):
            with patch("lf_toolkit.evaluation.progress.requests.post") as mock_post:
                mock_post.return_value = Mock(ok=True)
                evaluation_function("A n B", "A n B", Params())
                _wait_for_progress_executor()

        self.assertEqual(mock_post.call_count, 2)

        first_call, second_call = mock_post.call_args_list
        self.assertEqual(
            first_call.kwargs["json"],
            {"message": "Parsing response and answer..."},
        )
        self.assertEqual(
            second_call.kwargs["json"],
            {"message": "Comparing sets for equivalence..."},
        )


if __name__ == "__main__":
    unittest.main()

from typing import Any
from sympy import simplify_logic, Equivalent
from lf_toolkit.evaluation import Result, Params
from lf_toolkit.parse.set import SetParser, LatexPrinter, SymPyBooleanTransformer, ASCIIPrinter

# TODO: this is hacky, we need another way to bundle up everything.
try:
    from .parse import parse_with_feedback, FeedbackException
except:
    from parse import parse_with_feedback, FeedbackException

def evaluation_function(response: Any, answer: Any, params: Params, include_test_data: bool = False) -> dict:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    parser = SetParser.instance()
    sympyTransformer = SymPyBooleanTransformer()

    # here we want to compare the response set with the example solution set.
    # we have to do the following steps

    try:
        # 1. convert the `response`, which may be a latex string, to a sympy expression
        responseSet = parse_with_feedback(response, latex=params.get("is_latex", False))
        responseSetSympy = sympyTransformer.transform(responseSet)

        # 2. convert the `answer`, which may be a latex string, to a sympy expression
        # TODO: what if answer is also in latex? how do we know?
        answerSet = parser.parse(answer, latex=False)
        answerSetSympy = sympyTransformer.transform(answerSet)

        # 3. TODO: compare the two sympy expressions w/ simplification enabled. If they are equal, the sets produced by the two expressions are equal. However, the expressions may not be equal.
        # 4. compare the two sympy expressions w/ simplifaction disabled. If they are equal, the expressions are also equal.
        # 5a. TODO: If `params.enforce_expression_equality` is True, `is_correct` is True iff both 3) and 4) are True.
        # 5b. If `params.enforce_expression_equality` is False, `is_correct` is True iff 3) is True.
        result = simplify_logic(Equivalent(responseSetSympy, answerSetSympy))
        is_correct = result == True

        latexPrinter = LatexPrinter()
        latex = latexPrinter.print(responseSet)

        asciiPrinter = ASCIIPrinter()
        ascii = asciiPrinter.print(responseSet)

        return Result(
            is_correct=is_correct,
            latex=latex,
            simplified=ascii,
        ).to_dict(include_test_data=include_test_data)
    except FeedbackException as e:
        return Result(
            is_correct=False,
            feedback_items=[("parse_error", str(e))]
        ).to_dict(include_test_data)
    except Exception as e:
        return Result(
            is_correct=False,
            feedback_items=[("error", str(e))]
        ).to_dict(include_test_data)
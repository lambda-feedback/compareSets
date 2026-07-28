import logging
from typing import Any
from sympy import simplify_logic, Equivalent
from lf_toolkit.evaluation import Result, Params
from lf_toolkit.parse.set import SetParser, LatexPrinter, SymPyBooleanTransformer, ASCIIPrinter, SymPyTransformer

from .parse import parse_with_feedback, FeedbackException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s [%(name)s] %(message)s")

def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> dict:
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

    logger.debug("evaluation_function called")
    logger.debug("response type=%s value=%r", type(response).__name__, response)
    logger.debug("answer   type=%s value=%r", type(answer).__name__, answer)
    logger.debug("params   value=%r", params)

    parser = SetParser.instance()

    # here we want to compare the response set with the example solution set.
    # we have to do the following steps

    try:
        is_latex = params.get("is_latex", False)
        is_set_notation = params.get("is_set_notation", False)
        transformer = SymPyTransformer() if is_set_notation else SymPyBooleanTransformer()
        logger.debug("is_latex=%r", is_latex)
        logger.debug("is_set_notation=%r", is_set_notation)

        # 1. convert the `response`, which may be a latex string, to a sympy expression
        logger.debug("parsing response...")
        responseSet = parse_with_feedback(response, latex=is_latex)
        logger.debug("responseSet=%r", responseSet)
        responseSetSympy = transformer.transform(responseSet)
        logger.debug("responseSetSympy=%r", responseSetSympy)

        # 2. convert the `answer`, which may be a latex string, to a sympy expression
        # TODO: what if answer is also in latex? how do we know?
        logger.debug("parsing answer...")
        try:
            answerSet = parser.parse(answer, latex=False)
        except Exception as e:
            logger.error("failed to parse answer: type=%s value=%r error=%r", type(answer).__name__, answer, e)
            raise FeedbackException() from e
        logger.debug("answerSet=%r", answerSet)
        answerSetSympy = transformer.transform(answerSet)
        logger.debug("answerSetSympy=%r", answerSetSympy)

        # 3. compare the two sympy expressions w/ simplification enabled.
        #    If they are equal, the sets produced by the two expressions are
        #    semantically equal. However, the expressions may not be equal.
        if is_set_notation:
            semantic_equal = responseSetSympy == answerSetSympy
        else:
            semantic_equal = simplify_logic(Equivalent(responseSetSympy, answerSetSympy)) == True
        logger.debug("semantic_equal=%r", semantic_equal)

        # 4. compare the two sympy expressions w/ simplifaction disabled.
        #    If they are equal, the expressions are also equal in syntax.
        #    This respects laws of commutativity, e.g. A u B == B u A.
        syntactic_equal = responseSetSympy == answerSetSympy
        logger.debug("syntactic_equal=%r", syntactic_equal)

        enforce_expression_equality = params.get("enforce_expression_equality", False)
        logger.debug("enforce_expression_equality=%r", enforce_expression_equality)

        # 5. `is_correct` is True, iff 3) is True, and either 4) or `enforce_expression_equality` is True
        is_correct = semantic_equal and (syntactic_equal or not enforce_expression_equality)
        logger.debug("is_correct=%r", is_correct)

        feedback_items=[]

        if semantic_equal and not syntactic_equal and enforce_expression_equality:
            feedback_items.append(("syntactic_equality", "The expressions are not equal syntacitcally."))
        elif not semantic_equal:
            feedback_items.append(("semantic_equality", "The expressions are not equal."))

        latexPrinter = LatexPrinter()
        latex = latexPrinter.print(responseSet)

        asciiPrinter = ASCIIPrinter()
        ascii = asciiPrinter.print(responseSet)

        return Result(
            is_correct=is_correct,
            latex=latex,
            simplified=ascii,
            feedback_items=feedback_items,
        )
    except FeedbackException as e:
        logger.error("FeedbackException: %r", e)
        return Result(
            is_correct=False,
            feedback_items=[("parse_error", str(e))]
        )

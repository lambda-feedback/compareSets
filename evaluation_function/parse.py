from lf_toolkit.parse.set import SetParser, ParseError

# Subclasses ValueError so that, when raised from the evaluation function,
# lf_toolkit reports it as an invalid submission (422) rather than a 500.
class FeedbackException(ValueError):

    def __str__(self):
        if isinstance(self.__cause__, ParseError):
            return str(self.__cause__)
        else:
            return "Evaluation failed"


def parse_with_feedback(response: str, latex: bool = False):
    try:
        parser = SetParser.instance()
        return parser.parse(response, latex=latex)
    except Exception as e:
        raise FeedbackException() from e

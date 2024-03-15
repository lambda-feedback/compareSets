from lf_toolkit.parse.set import SetParser, ParseError

class FeedbackException(Exception):

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

from typing import Any
from lf_toolkit.preview import Result, Params, Preview
from lf_toolkit.parse.set import SetParser, LatexPrinter, ASCIIPrinter

def preview_function(response: Any, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """

    parser = SetParser.instance()
    result = parser.parse(response, latex=params.is_latex)

    latexPrinter = LatexPrinter()
    latex = latexPrinter.print(result)

    asciiPrinter = ASCIIPrinter()
    ascii = asciiPrinter.print(result)

    preview = Preview(
        latex=latex,
        sympy=ascii,
        feedback="",
    )

    return Result(preview=preview)

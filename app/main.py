from sympy import Union, Symbol, Interval, FiniteSet
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.pretty import pretty





if __name__ == "__main__":
    # response = "A nn B"
    # result = parse_expr(response)

    result = parse_expr("A OR B")
    
    # sympy1 = Union(FiniteSet(Symbol("x")), FiniteSet(Symbol("y")))

    # sympy2 = Union(FiniteSet(Symbol("y")), FiniteSet(Symbol("x")))

    # print(sympy1 == sympy2)

    print(type(result))
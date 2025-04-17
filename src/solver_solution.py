SolverFloats = tuple[float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float]

class SolverSolution:
    """
    Represents a potential solution that the solver has generated.

    The input variables are the variables in VehicleTrip,
    except for fuel efficiency, which is the output.

    The solution has the following for each input variable:
    - a fifth order polynomial `a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f`
    - a reciprocal `a/(x+b)`
    - a rational function `(a*x^3 + b*x^2 + c*x + d) / (e*x^3 + f*x^2 + g*x + h)`
    - an exponent `a*b^x + c*x*d^x`
    - a logarithm `a*log_b(x) + c*b*log_d(x)`
    - five trigonometric functions `a*sin(b*x + c) + d*sin(e*x + f) + ...`

    This brings the total solution variable count to 40 per input variable.
    """
    def __init__(self, solution_parameters: SolverFloats):
        self.__solution_parameters: SolverFloats = solution_parameters

    @property
    def solution_parameters(self) -> SolverFloats:
        return self.__solution_parameters

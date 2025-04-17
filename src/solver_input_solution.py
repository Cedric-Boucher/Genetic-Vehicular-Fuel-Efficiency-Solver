from math import log, sin
from scipy.stats import norm

SolverFloats = tuple[float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float]

def bounded_to_gauss(x: float, mean: float = 0.0, standard_deviation: float = 10.0) -> float:
    # Clamp x into the open interval (0, 1)
    eps = 1e-10
    u = min(max(x, eps), 1 - eps)

    assert (u > 0 and u < 1), "provided x value was outside of allowable range [0, 1] for conversion via gaussian function"

    # Convert to Gaussian
    percent_point = float(norm.ppf(u))
    return percent_point * standard_deviation + mean

class SolverInputSolution:
    """
    Represents a potential solution that the solver has generated for a single input variable.

    The solution has the following:
    - a fifth order polynomial `a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f`
    - a reciprocal `a/(x+b)`
    - a rational function `(a*x^3 + b*x^2 + c*x + d) / (e*x^3 + f*x^2 + g*x + h)`
    - a logarithm `a*log_b(x) + c*x*log_d(x)`
    - five trigonometric functions `a*sin(b*x + c) + d*sin(e*x + f) + ...`
    - an exponent `a*b^x + c*x*d^x`

    This brings the total solution variable count to 39.
    """
    def __init__(self, solution_parameters: SolverFloats):
        """
        args:
            solution_parameters: SolverFloats - each of these values MUST be in the range [0, 1] (bounds can be inclusive or exclusive)
        """
        self.__solution_parameters: SolverFloats = solution_parameters

    @property
    def solution_parameters(self) -> SolverFloats:
        return self.__solution_parameters

    def f(self, x: float) -> float:
        if x <= 0:
            raise Exception("Input value x is expected to be a positive and non-zero scalar value, but was negative or 0")
        p: SolverFloats = SolverFloats([bounded_to_gauss(v) for v in self.__solution_parameters])
        y: float = p[0]*x**5 + p[1]*x**4 + p[2]*x**3 +  p[3]*x**2 + p[4]*x + p[5]
        if (x+p[7]) != 0:
            y += p[6]/(x+p[7])
        if (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15]) != 0:
            y += (p[8]*x**3 + p[9]*x**2 + p[10]*x + p[11]) / (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15])
        if p[17] != 1 and p[17] > 0:
            y += p[16]*log(x, p[17])
        if p[19] != 1 and p[19] > 0:
            y += p[18]*x*log(x, p[19])
        y += p[20]*sin(p[21]*x + p[22]) + p[23]*sin(p[24]*x + p[25]) + p[26]*sin(p[27]*x + p[28])
        y += p[29]*sin(p[30]*x + p[31]) + p[32]*sin(p[33]*x + p[34])
        y += p[35]*p[36]**x + p[37]*x*p[38]**x

        return y

if __name__ == "__main__":
    from random import random, gauss
    test = SolverSolutionInput(tuple(random() for _ in range(39))) # type: ignore
    print(test.f(1))

from math import log, sin
from scipy.stats import norm
import config

import warnings

warnings.filterwarnings("error", category=RuntimeWarning)

SolverFloats = tuple[float, ...]

STANDARD_DEVIATION_MULTIPLIER: float = 100.0

def bounded_to_gauss(x: float, mean: float = 0.0, standard_deviation: float = 1.0) -> float:
    # Clamp x into the open interval (0, 1)
    eps = 1e-10
    u = min(max(x, eps), 1 - eps)

    assert (u > 0 and u < 1), "provided x value was outside of allowable range [0, 1] for conversion via gaussian function"

    # Convert to Gaussian
    percent_point = float(norm.ppf(u))
    gaussian: float = percent_point * standard_deviation + mean
    assert isinstance(gaussian, float)
    return gaussian

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
    - standard deviation to use for gaussian function

    This brings the total solution variable count to 40.
    """
    def __init__(self, solution_parameters: SolverFloats):
        """
        args:
            solution_parameters: SolverFloats - each of these values MUST be in the range [0, 1] (bounds can be inclusive or exclusive)
        """
        assert isinstance(solution_parameters, tuple)
        assert len(solution_parameters) == config.GENES_PER_VARIABLE
        self.__solution_parameters: SolverFloats = solution_parameters

    @property
    def solution_parameters(self) -> SolverFloats:
        return self.__solution_parameters

    def f(self, x: float) -> float:
        if x == 0:
            x = 0.000000001
        if x <= 0:
            raise Exception("Input value x is expected to be a positive and non-zero scalar value, but was negative or 0")
        raw_solution_parameters: list[float] = [self.__solution_parameters[i] for i in range(0, len(self.__solution_parameters), 2)]
        standard_deviations: list[float] = [self.__solution_parameters[i+1]*STANDARD_DEVIATION_MULTIPLIER for i in range(0, len(self.__solution_parameters), 2)]
        solution_parameters: list[tuple[float, float]] = list(zip(raw_solution_parameters, standard_deviations, strict=True))
        p: SolverFloats = SolverFloats([bounded_to_gauss(v, std) for (v, std) in solution_parameters])
        y: float = p[0]*x**5 + p[1]*x**4 + p[2]*x**3 +  p[3]*x**2 + p[4]*x + p[5]
        if (x+p[7]) != 0:
            y += p[6]/(x+p[7])
        if (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15]) != 0:
            y += (p[8]*x**3 + p[9]*x**2 + p[10]*x + p[11]) / (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15])
        if p[17] != 1:
            y += p[16]*log(x, abs(p[17]))
        if p[19] != 1:
            y += p[18]*x*log(x, abs(p[19]))
        y += p[20]*sin(p[21]*x + p[22]) + p[23]*sin(p[24]*x + p[25]) + p[26]*sin(p[27]*x + p[28])
        y += p[29]*sin(p[30]*x + p[31]) + p[32]*sin(p[33]*x + p[34])
        try:
            y += p[35]*p[36]**x + p[37]*x*p[38]**x
            y = y.real # y may be complex after this part since p[36] or p[38] may be negative and x may not be a whole number
        except OverflowError:
            pass
        except RuntimeWarning:
            pass

        assert isinstance(y, float)
        return y

    def __str__(self) -> str:
        raw_solution_parameters: list[float] = [self.__solution_parameters[i] for i in range(0, len(self.__solution_parameters), 2)]
        standard_deviations: list[float] = [self.__solution_parameters[i+1]*STANDARD_DEVIATION_MULTIPLIER for i in range(0, len(self.__solution_parameters), 2)]
        solution_parameters: list[tuple[float, float]] = list(zip(raw_solution_parameters, standard_deviations, strict=True))
        p: SolverFloats = SolverFloats([bounded_to_gauss(v, std) for (v, std) in solution_parameters])
        equation_string: str = str(
            "{p0:.2f}*x^5 + {p1:.2f}*x^4 + {p2:.2f}*x^3 + {p3:.2f}*x^2 + {p4:.2f}*x + {p5:.2f} +\n"
            "{p6:.2f}/(x + {p7:.2f}) +\n"
            "({p8:.2f}*x^3 + {p9:.2f}*x^2 + {p10:.2f}*x + {p11:.2f}) / ({p12:.2f}*x^3 + {p13:.2f}*x^2 + {p14:.2f}*x + {p15:.2f}) +\n"
            "{p16:.2f}*log_{p17:.2f}(x) + {p18:.2f}*x*log_{p19:.2f}(x) +\n"
            "{p20:.2f}*sin({p21:.2f}*x + {p22:.2f}) + {p23:.2f}*sin({p24:.2f}*x + {p25:.2f}) + {p26:.2f}*sin({p27:.2f}*x + {p28:.2f}) + {p29:.2f}*sin({p30:.2f}*x + {p31:.2f}) + {p32:.2f}*sin({p33:.2f}*x + {p34:.2f}) +\n"
            "Re({p35:.2f}*({p36:.2f})^x + {p37:.2f}*x*({p38:.2f})^x)"
        ).format(
            p0 = p[0],
            p1 = p[1],
            p2 = p[2],
            p3 = p[3],
            p4 = p[4],
            p5 = p[5],
            p6 = p[6],
            p7 = p[7],
            p8 = p[8],
            p9 = p[9],
            p10 = p[10],
            p11 = p[11],
            p12 = p[12],
            p13 = p[13],
            p14 = p[14],
            p15 = p[15],
            p16 = p[16],
            p17 = p[17],
            p18 = p[18],
            p19 = p[19],
            p20 = p[20],
            p21 = p[21],
            p22 = p[22],
            p23 = p[23],
            p24 = p[24],
            p25 = p[25],
            p26 = p[26],
            p27 = p[27],
            p28 = p[28],
            p29 = p[29],
            p30 = p[30],
            p31 = p[31],
            p32 = p[32],
            p33 = p[33],
            p34 = p[34],
            p35 = p[35],
            p36 = p[36],
            p37 = p[37],
            p38 = p[38]
        )

        return equation_string

if __name__ == "__main__":
    from random import random
    test = SolverInputSolution(tuple(random() for _ in range(39))) # type: ignore
    print(test.f(1))

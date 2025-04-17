from math import log, sin

SolverFloats = tuple[float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float, float,
                     float, float, float, float, float, float, float, float, float]

class SolverSolution:
    """
    Represents a potential solution that the solver has generated.

    The input variables are the variables in VehicleTrip,
    except for fuel efficiency, which is the output.

    The solution has the following for each input variable:
    - a fifth order polynomial `a*x^5 + b*x^4 + c*x^3 + d*x^2 + e*x + f`
    - a reciprocal `a/(x+b)`
    - a rational function `(a*x^3 + b*x^2 + c*x + d) / (e*x^3 + f*x^2 + g*x + h)`
    - a logarithm `a*log_b(x) + c*x*log_d(x)`
    - five trigonometric functions `a*sin(b*x + c) + d*sin(e*x + f) + ...`
    - an exponent `a*b^x + c*x*d^x`

    This brings the total solution variable count to 39 per input variable.
    """
    def __init__(self, solution_parameters: SolverFloats):
        self.__solution_parameters: SolverFloats = solution_parameters

    @property
    def solution_parameters(self) -> SolverFloats:
        return self.__solution_parameters

    def f(self, x: float) -> float:
        if x <= 0:
            raise Exception("Input value x is expected to be a positive and non-zero scalar value, but was negative or 0")
        p: SolverFloats = self.__solution_parameters # just to make it shorter and easier to read
        y: float = p[0]*x**5 + p[1]*x**4 + p[2]*x**3 +  p[3]*x**2 + p[4]*x + p[5]
        if (x+p[7]) != 0:
            y += p[6]/(x+p[7])
        if (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15]) != 0:
            y += (p[8]*x**3 + p[9]*x**2 + p[10]*x + p[11]) / (p[12]*x**3 + p[13]*x**2 + p[14]*x + p[15])
        y += p[16]*log(x, p[17]) + p[18]*x*log(x, p[19])
        y += p[20]*sin(p[21]*x + p[22]) + p[23]*sin(p[24]*x + p[25]) + p[26]*sin(p[27]*x + p[28])
        y += p[29]*sin(p[30]*x + p[31]) + p[32]*sin(p[33]*x + p[34])
        y += p[35]*p[36]**x + p[37]*x*p[38]**x

        return y

if __name__ == "__main__":
    from random import random
    test = SolverSolution(tuple(random() for _ in range(39)))
    print(test.f(1))


# problem is that values only have the range 0-1 but we want them to be unbounded...

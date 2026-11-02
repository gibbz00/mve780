import math
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import tabulate as tab


def part_1_b():
    f = lambda x: np.e**x
    a = 0
    b = 1
    expected = np.e - 1
    n_list = [2**x for x in range(2, 7)]

    perform_riemann(f, a, b, expected, n_list)


def part_1_c():
    f = lambda x: np.sin(x)
    a = 0
    b = np.pi
    expected = 2
    n_list = [10**x for x in range(1, 4)]

    perform_riemann(f, a, b, expected, n_list)


def part_2_b():
    f = lambda x: 1 / x
    a = 1
    b = 2
    expected = np.log(2)
    n_list = [2**x for x in range(1, 11)]

    _fig, ax = plt.subplots()
    approximators = [
        (riemann, "Riemann Midpoint"),
        (trapezoidal, "Trapezoidal Rule"),
        (simpsons, "Simpsons Rule"),
    ]

    for approximator, name in approximators:
        # Pre-allocate with expected capacity
        errors = np.zeros(len(n_list))

        for i, n in enumerate(n_list):
            approximation = approximator(f, a, b, n)
            errors[i] = np.abs(expected - approximation)

        ax.loglog(n_list, errors, "o-", label=name)

    ax.set_xlabel("x")
    ax.set_ylabel("error")
    ax.grid(True)
    ax.legend()

    plt.show()


def part_3_b():
    f = lambda x: np.e ** (-(x**2))
    (value, iterations) = integral(f, 0, 2, 1e-10, 30)
    sigmoid = math.sqrt(math.pi) / 2.0 * math.erf(2)
    error = np.abs(sigmoid - value)

    print(
        f"value: {value}, iterations: {iterations}, expected: {sigmoid}, error: {error}"
    )


def integral(
    f, a: float, b: float, tolerance: float, max_iter: int
) -> tuple[float, int]:
    i = 1
    current = simpsons(f, a, b, 2**i)

    while i < max_iter:
        i += 1
        previous = current
        current = simpsons(f, a, b, 2**i)

        if np.abs(previous - current) < tolerance:
            break

    return (current, i)


def simpsons(f, a: float, b: float, n: int) -> float:
    t_1 = trapezoidal(f, a, b, n // 2)
    t_2 = trapezoidal(f, a, b, n)
    return (4 * t_2 - t_1) / 3.0


def trapezoidal(f, a: float, b: float, n: int) -> float:
    width = (b - a) / n
    x = a + width * np.arange(n + 1)
    y = f(x)

    # All but the first and last value have two halves present.
    return width * (np.sum(y) - (y[0] + y[n]) / 2.0)


class Method(Enum):
    Left = 0
    Right = 1
    Center = 2


def riemann(f, a: float, b: float, n: int, method: Method = Method.Center) -> float:
    width = (b - a) / n
    x = None

    match method:
        case Method.Left:
            x = a + width * np.arange(n)
        case Method.Right:
            x = a + width * np.arange(1, n + 1)
            print()
        case Method.Center:
            # x = a + h/2 + h * n <==> a + h(n + 1/2)
            x = a + width * (np.arange(n) + 1 / 2)

    return width * np.sum(f(x))


def perform_riemann(f, a, b, expected, n_list):
    rows = []

    for n in n_list:
        columns = [n]

        for method in Method:
            result = riemann(f, a, b, n, method)
            error = np.abs(result - expected)
            columns.append(error)

        rows.append(columns)

    print(
        tab.tabulate(
            rows,
            headers=["n"] + list(Method),
            tablefmt="simple_outline",
            floatfmt=".2e",
        )
    )


if __name__ == "__main__":
    part_1_b()
    part_1_c()
    part_2_b()
    part_3_b()

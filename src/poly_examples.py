import argparse

from sympy import poly
from sympy.polys.polyfuncs import interpolate
from sympy.abc import x
from sympy.plotting import plot
from sympy.printing import latex


def genpis(n):
    polys = []
    # Make P_0
    points = [(i+1, -1) for i in range(n-1)]
    points.append((n, 0))
    poly_i = poly(interpolate(points, x))
    polys.append(poly_i)
    # Make P_i
    for i in range(n-1):
        points = []
        for j in range(n-1):
            if i == j:
                points.append((j+1, 2))
            else:
                points.append((j+1, 0))
        points.append((n, 1))
        poly_i = poly(interpolate(points, x))
        polys.append(poly_i)
    return polys


def genhpis(n):
    polys = []
    hpi = poly(x**(n+1))
    polys = [hpi**(i+1) for i in range(1, n+1)]
    return polys


def draw_poly(p):
    plot(p.as_expr())


def eval_poly(p, x, m):
    return p.eval(x) % m


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int, default=3,
                    help="number of polynomials")
parser.add_argument("-x", "--x", type=int, default=6,
                    help="x value to evaluate")
parser.add_argument("-m", "--modulo", type=int, default=7,
                    help="modulo to use for reduction evaluation")
parser.add_argument("-t", "--tah", action="store_true",
                    help="generate hat polynomials", default=False)
parser.add_argument("-d", "--draw", action="store_true",
                    help="draw polynomials", default=False)
args = parser.parse_args()

if args.tah:
    polys = genhpis(args.number)
else:
    polys = genpis(args.number)

for p in polys:
    print(p)
    print(eval_poly(p, args.x, args.modulo))

if args.draw:
    for p in polys:
        plot(p.as_expr(), title="$" + latex(p.as_expr()) + "$", ylabel="")

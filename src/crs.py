from libffpy import LibffPy
from collections import namedtuple
from pisgen import generate_pis, generate_pi_hats


gk_T = namedtuple("gk_T", ["G", "q", "g1", "g2", "gt", "e"])
Chi_T = namedtuple("Chi_T",
                   ["chi", "alpha", "beta", "betahat", "rho", "rhohat", "sk"])

CRS_1SP_T = namedtuple(
    "CRS_1SP_T", [
        "g1_alpha_poly_zero", "g1_poly_zero", "g1_poly_squares",
        "g1_sum", "g1_hat_sum",
        "g2alpha", "g2_sum",
        "pair_alpha"])

CRS_SM_T = namedtuple(
    "CRS_SM_T", ["g1_beta_polys", "g1_beta_rhos",
                 "g2_beta", "g2_betahat"])

CRS_CON_T = namedtuple(
    "CRS_SM_T", ["g1_poly_hats", "g1rhohat"])

CRS_T = namedtuple(
    "CRS_T", ["gk", "pk", "g1_polys", "g1rho", "g2_polys", "g2rho",
              "crs_sm", "crs_1sp", "crs_con"])


def mk_gk(n):
    G = LibffPy(n)
    q = G.order()
    g1 = G.gen1()
    g2 = G.gen2()
    gt = G.pair(g1, g2)
    return gk_T(G, q, g1, g2, gt, G.pair)


def mk_Chi(q):
    chi = q.random()
    alpha = q.random()
    beta = q.random()
    betahat = q.random()
    rho = 1 + (q - 1).random()
    rhohat = 1 + (q - 1).random()
    sk = q.random()
    return Chi_T(chi, alpha, beta, betahat, rho, rhohat, sk)


def mk_crs_1sp(gk, Chi, polys, poly_zero, poly_hats):
    # common values
    poly_sum = sum(polys)
    poly_hat_sum = sum(poly_hats)

    # G1
    g1_alpha_poly_zero = (Chi.alpha + poly_zero) * gk.g1
    g1_poly_zero = poly_zero * gk.g1
    inv_rho = Chi.rho.mod_inverse()
    g1_poly_squares = []
    for poly in polys:
        numer = (poly + poly_zero) ** 2 - 1
        g1_poly_squares.append((numer * inv_rho) * gk.g1)
    g1_sum = poly_sum * gk.g1
    g1_hat_sum = poly_hat_sum * gk.g1

    # G2
    g2alpha = (-Chi.alpha + poly_zero) * gk.g2
    g2_sum = poly_sum * gk.g2

    # GT
    pair_alpha = gk.gt ** (1 - Chi.alpha ** 2)

    return CRS_1SP_T(g1_alpha_poly_zero, g1_poly_zero, g1_poly_squares,
                     g1_sum, g1_hat_sum,
                     g2alpha, g2_sum,
                     pair_alpha)


def mk_crs_sm(gk, Chi, polys, poly_hats):
    # G1
    g1_beta_polys = []
    for poly, poly_hat in zip(polys, poly_hats):
        g1_beta_polys.append(
            (Chi.beta * poly + Chi.betahat * poly_hat) * gk.g1)
    g1_beta_rhos = (Chi.beta * Chi.rho + Chi.betahat * Chi.rhohat) * gk.g1

    # G2
    g2_beta = Chi.beta * gk.g2
    g2_betahat = Chi.betahat * gk.g2
    return CRS_SM_T(g1_beta_polys, g1_beta_rhos,
                    g2_beta, g2_betahat)


def mk_crs_con(gk, Chi, poly_hats):
    # G1
    g1_poly_hats = list(map(lambda poly_hat: poly_hat * gk.g1, poly_hats))
    g1rhohat = Chi.rhohat * gk.g1
    return CRS_CON_T(g1_poly_hats, g1rhohat)


def mk_crs(n, gk, Chi):
    polys_all = generate_pis(Chi.chi, n)
    poly_zero = polys_all[0]
    polys = polys_all[1:]
    poly_hats = generate_pi_hats(Chi.chi, n, gk.q)

    pk = (gk.g2, Chi.sk * gk.g2)
    g1_polys = list(map(lambda poly: poly * gk.g1, polys))
    g1rho = Chi.rho * gk.g1
    g2_polys = list(map(lambda poly: poly * gk.g2, polys))
    g2rho = Chi.rho * gk.g2

    crs_sm = mk_crs_sm(gk, Chi, polys, poly_hats)
    crs_1sp = mk_crs_1sp(gk, Chi, polys, poly_zero, poly_hats)
    crs_con = mk_crs_con(gk, Chi, poly_hats)
    crs = CRS_T(gk, pk, g1_polys, g1rho, g2_polys, g2rho,
                crs_sm, crs_1sp, crs_con)
    trapdoor = (Chi.chi, Chi. rhohat)
    return crs, trapdoor

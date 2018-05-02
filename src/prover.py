from libffpy import G1Py, G2Py
from elgamal import enc
from numpy import array
import datetime


def inverse_perm(s):
    r = [None] * len(s)
    for index, value in enumerate(s):
        r[value] = index
    return r


def step1a(n, q, g1rho):
    randoms = [q.random() for i in range(n - 1)]
    g1_randoms = list(map(lambda random: random * g1rho, randoms))
    return randoms, g1_randoms


def step1b(sigma, randoms, g1_randoms,
           g1_polys, g1_poly_hats, g2_polys, g2rho, g1rhohat):
    A = []
    B = []
    A_hat = []
    inverted_sigma = inverse_perm(sigma)

    #  g1_polys = array(map(lambda perm_i: g1_polys[perm_i], inverted_sigma))
    #  g2_polys = array(map(lambda perm_i: g2_polys[perm_i], inverted_sigma))
    #  g1_poly_hats = array(map(lambda perm_i: g1_poly_hats[perm_i], inverted_sigma))
    #  g1_randoms = array(g1_randoms)
    #  randoms_g2_rho = array(map(lambda random: random * g2rho, randoms))  #  extra step
    #  randoms_g1rhohat = array(map(lambda random: random * g1rhohat, randoms))
    #  A = list(g1_polys[:-1] + g1_randoms)
    #  B = list(g2_polys[:-1] + randoms_g2_rho)
    #  A_hat = list(g1_poly_hats[:-1] + randoms_g1rhohat)

    start = datetime.datetime.now()

    #  g1_polys = array(g1_polys)
    #  A = list(g1_polys[inverted_sigma][:-1] + g1_randoms)

    #  g2_polys = array(g2_polys)
    #  randoms = array(randoms)
    #  randoms_g2rho = randoms * g2rho
    #  B = list(g2_polys[inverted_sigma][:-1] + randoms_g2rho)

    #  g1_poly_hats = array(g1_poly_hats)
    #  randoms_g1rhohat = randoms * g1rhohat
    #  A_hat = list(g1_poly_hats[inverted_sigma][:-1] + randoms_g1rhohat)

    #  start = datetime.datetime.now()
    #  A = g1_polys[inverted_sigma][:-1] + g1_randoms
    #  randoms_g2rho = randoms * g2rho
    #  B = g2_polys[inverted_sigma][:-1] + randoms_g2rho
    #  randoms_g1rhohat = randoms * g1rhohat
    #  A_hat = g1_poly_hats[inverted_sigma][:-1] + randoms_g1rhohat

    for perm_i, g1_random, random in zip(inverted_sigma, g1_randoms, randoms):
        A.append(g1_polys[perm_i] + g1_random)
        B.append(g2_polys[perm_i] + random * g2rho)
        A_hat.append(g1_poly_hats[perm_i] + random * g1rhohat)

    total = datetime.datetime.now() - start

    return A, B, A_hat


def get_infs():
    inf1 = G1Py.inf()
    inf2 = G2Py.inf()
    return inf1, inf2


def step2(gk, A, B, g1_sum, g2_sum):
    inf1, inf2 = get_infs()
    A.append(g1_sum - sum(A, inf1))
    B.append(g2_sum - sum(B, inf2))
    return A, B


def step3(gk, A_hat, g1_hat_sum):
    inf1, inf2 = get_infs()
    A_hat.append(g1_hat_sum - sum(A_hat, inf1))
    return A_hat


def step4(gk, randoms, g1_randoms, g1rho):
    rand_n = - sum(randoms)
    randoms.append(rand_n)
    g1_randoms.append(rand_n * g1rho)
    return randoms, g1_randoms


def step5a(randoms, A, g1_randoms, sigma, g1_poly_zero, g1_poly_squares):
    C = []
    inverted_sigma = inverse_perm(sigma)
    for random, a, g1_random, perm_i in zip(
            randoms, A, g1_randoms, inverted_sigma):
        C.append(random * (2 * (a + g1_poly_zero) - g1_random) +
                 g1_poly_squares[perm_i])
    return C


def step5b(sigma, randoms, g1_beta_polys, g1_beta_rhos):
    D = []
    inverted_sigma = inverse_perm(sigma)
    for perm_i, random in zip(inverted_sigma, randoms):
        D.append(g1_beta_polys[perm_i] + random * g1_beta_rhos)
    return D


def step6(gk, t_randoms, g1_poly_hats, g1rhohat):
    rt = gk.q.random()
    inf1, _ = get_infs()
    g1_t = rt * g1rhohat
    for t_random, g1_poly_hat in zip(t_randoms, g1_poly_hats):
        g1_t += t_random * g1_poly_hat
    return rt, g1_t


def step7(gk, sigma, t_randoms, pk, ciphertexts):
    _, inf2 = get_infs()
    M_primes = []
    for perm_i, t_random in zip(sigma, t_randoms):
        M_primes.append(tuple_add(ciphertexts[perm_i], enc(pk, t_random, 0)))
    return M_primes


def tuple_map(func, tpl):
    return tuple(map(func, tpl))


def tuple_add(tpl1, tpl2):
    zipped = zip(tpl1, tpl2)
    return tuple(z[0] + z[1] for z in zipped)


def step8(pk, rt, randoms, ciphertexts):
    N = tuple_map(lambda elem: rt * elem, pk)
    for random, ciphertext in zip(randoms, ciphertexts):
        N = tuple_add(N, tuple_map(lambda elem: random * elem, ciphertext))
    return N


def step9(B, C):
    return B[:-1], C


def step10(D):
    return D


def step11(A_hat, g1_t, N):
    return A_hat[:-1], g1_t, N


def step12(M_primes, A, pi_1sp, pi_sm, pi_con):
    return M_primes, A[:-1], pi_1sp, pi_sm, pi_con


def prove(n, crs, ciphertexts, sigma, t_randoms):
    randoms, g1_randoms = step1a(n, crs.gk.q, crs.g1rho)
    A, B, A_hat = step1b(
        sigma, randoms, g1_randoms,
        crs.g1_polys, crs.crs_con.g1_poly_hats,
        crs.g2_polys, crs.g2rho, crs.crs_con.g1rhohat)
    A, B = step2(crs.gk, A, B, crs.crs_1sp.g1_sum, crs.crs_1sp.g2_sum)
    A_hat = step3(crs.gk, A_hat, crs.crs_1sp.g1_hat_sum)
    randoms, g1_randoms = step4(crs.gk, randoms, g1_randoms, crs.g1rho)
    C = step5a(randoms, A, g1_randoms, sigma,
               crs.crs_1sp.g1_poly_zero, crs.crs_1sp.g1_poly_squares)
    D = step5b(
        sigma, randoms, crs.crs_sm.g1_beta_polys, crs.crs_sm.g1_beta_rhos)
    rt, g1_t = step6(
        crs.gk, t_randoms, crs.crs_con.g1_poly_hats, crs.crs_con.g1rhohat)
    M_primes = step7(crs.gk, sigma, t_randoms, crs.pk, ciphertexts)
    N = step8(crs.pk, rt, randoms, ciphertexts)
    pi_1sp = step9(B, C)
    pi_sm = step10(D)
    pi_con = step11(A_hat, g1_t, N)
    pi_sh = step12(M_primes, A, pi_1sp, pi_sm, pi_con)
    return pi_sh

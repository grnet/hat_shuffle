from bplib.bp import GTElem
import prover
from functools import reduce


def step1(pi_sh):
    M_prime, g1_a, pi_1sp, pi_sm, pi_con = pi_sh
    g2_b, g1_c = pi_1sp
    g1_d = pi_sm
    g1_hat_a, g1_t, N = pi_con
    return M_prime, g1_a, pi_1sp, pi_sm, pi_con, \
        g2_b, g1_c, g1_d, g1_hat_a, g1_t, N


def step2(gk, g1_a, g2_b, g1_hat_a, g1_sum, g2_sum, g1_hat_sum):
    g1_a, g2_b = prover.step2(gk, g1_a, g2_b, g1_sum, g2_sum)
    g1_hat_a = prover.step3(gk, g1_hat_a, g1_hat_sum)
    return g1_a, g2_b, g1_hat_a


def get_infT(gk):
    return GTElem.one(gk.G)


def step3(gk, g1_a, g2_b, g1_c, crs_1sp, g2_rho):
    g1_alpha_poly_zero = crs_1sp.g1_alpha_poly_zero
    g2alpha = crs_1sp.g2alpha
    pair_alpha = crs_1sp.pair_alpha

    for a, b, c in zip(g1_a, g2_b, g1_c):
        left = gk.e(a + g1_alpha_poly_zero, b + g2alpha)
        right = gk.e(c, g2_rho) * pair_alpha
        if left != right:
            return False
    return True


def step3_batched(n, gk, g1_a, g2_b, g1_c, crs_1sp, g2_rho):
    y1 = [gk.q.random() for x in range(n - 1)] + [1]
    infT = get_infT(gk)
    inf1, _ = prover.get_infs(gk)

    g1_alpha_poly_zero = crs_1sp.g1_alpha_poly_zero
    g2alpha = crs_1sp.g2alpha
    pair_alpha = crs_1sp.pair_alpha

    right = (gk.e(mexp(y1, g1_c, inf1), g2_rho) *
             (pair_alpha ** (sum(y1) % gk.q)))
    left = infT
    for yi, a, b in zip(y1, g1_a, g2_b):
        left *= gk.e(yi * (a + g1_alpha_poly_zero), b + g2alpha)
    return left == right


def step4(gk, g1_d, g1_a, g1_hat_a, crs_sm):
    g2_beta = crs_sm.g2_beta
    g2_beta_hat = crs_sm.g2_betahat

    for d, a, ah in zip(g1_d, g1_a, g1_hat_a):
        left = gk.e(d, gk.g2)
        right = gk.e(a, g2_beta) * gk.e(ah, g2_beta_hat)
        if left != right:
            return False
    return True


def step4_batched(n, gk, g1_d, g1_a, g1_hat_a, crs_sm):
    y2 = [gk.q.random() for x in range(n - 1)] + [1]
    inf1, _ = prover.get_infs(gk)

    g2_beta = crs_sm.g2_beta
    g2_beta_hat = crs_sm.g2_betahat

    left = gk.e(mexp(y2, g1_d, inf1), gk.g2)
    right = (gk.e(mexp(y2, g1_a, inf1), g2_beta) *
             gk.e(mexp(y2, g1_hat_a, inf1), g2_beta_hat))
    return left == right


def step5(gk, pk, g1_t, crs_con, g1_a_hat, N, M, MP):
    infT = get_infT(gk)
    g1_hat_rho = crs_con.g1rhohat
    g1_poly_hats = crs_con.g1_poly_hats

    right = [gk.e(g1_t, pk[i]) * gk.e(g1_hat_rho, N[i]).inv()
             for i in range(2)]
    left = [infT, infT]
    for i in range(2):
        for ph, mp, a, m in zip(g1_poly_hats, MP, g1_a_hat, M):
            left[i] *= gk.e(ph, mp[i]) * gk.e(a, m[i]).inv()
    return left == right


def mexp(scals, elems, inf):  # find optimized version in lib
    return reduce(lambda x, y: x + y,
                  map(lambda tup: tup[0] * tup[1], zip(scals, elems)),
                  inf)


def step5_batched(gk, pk, g1_t, crs_con, g1_a_hat, N, M, MP):
    infT = get_infT(gk)
    _, inf2 = prover.get_infs(gk)
    g1_hat_rho = crs_con.g1rhohat
    g1_poly_hats = crs_con.g1_poly_hats
    y3 = [gk.q.random(), 1]

    q = gk.e(g1_t, mexp(y3, pk, inf2))
    right = q * gk.e(g1_hat_rho, mexp(y3, N, inf2)).inv()

    left = infT
    for ph, mp, a, m in zip(g1_poly_hats, MP, g1_a_hat, M):
        left *= gk.e(ph, mexp(y3, mp, inf2)) * gk.e(a, mexp(y3, m, inf2)).inv()
    return left == right


def verify_batched(n, crs, M, pi_sh):
    print("Using Batching")
    M_prime, g1_a, pi_1sp, pi_sm, \
        pi_con, g2_b, g1_c, g1_d, g1_hat_a, g1_t, N = step1(pi_sh)

    g1_a, g2_b, g1_hat_a = step2(
        crs.gk, g1_a, g2_b, g1_hat_a, crs.crs_1sp.g1_sum,
        crs.crs_1sp.g2_sum, crs.crs_1sp.g1_hat_sum)

    perm_ok = step3_batched(
        n, crs.gk, g1_a, g2_b, g1_c, crs.crs_1sp, crs.g2rho)
    sm_ok = step4_batched(n, crs.gk, g1_d, g1_a, g1_hat_a, crs.crs_sm)
    cons_ok = step5_batched(
        crs.gk, crs.pk, g1_t, crs.crs_con, g1_hat_a, N, M, M_prime)

    return perm_ok, sm_ok, cons_ok


def verify_non_batched(n, crs, M, pi_sh):
    print("Not Using Batching")

    M_prime, g1_a, pi_1sp, pi_sm, \
        pi_con, g2_b, g1_c, g1_d, g1_hat_a, g1_t, N = step1(pi_sh)

    g1_a, g2_b, g1_hat_a = step2(
        crs.gk, g1_a, g2_b, g1_hat_a, crs.crs_1sp.g1_sum,
        crs.crs_1sp.g2_sum, crs.crs_1sp.g1_hat_sum)

    perm_ok = step3(crs.gk, g1_a, g2_b, g1_c, crs.crs_1sp, crs.g2rho)
    sm_ok = step4(crs.gk, g1_d, g1_a, g1_hat_a, crs.crs_sm)
    cons_ok = step5(crs.gk, crs.pk, g1_t, crs.crs_con, g1_hat_a, N, M, M_prime)

    return perm_ok, sm_ok, cons_ok

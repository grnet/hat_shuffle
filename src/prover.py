from bplib.bp import G1Elem, G2Elem
from elgamal import enc


def inverse_perm(s):
    r = [None] * len(s)
    for index, value in enumerate(s):
        r[value] = index
    return r


def step_1a(n, q, g1_rho):
    randoms = [ q.random() for i in range(n - 1) ]
    g1_randoms = [ random * g1_rho for random in randoms ]
    hat_randoms = [ q.random() for i in range(n - 1) ]
    g1_hat_randoms = [ random * g1_rho for random in randoms ]
    return randoms, g1_randoms, hat_randoms, g1_hat_randoms


def step_1b(sigma, randoms, g1_randoms, hat_randoms, g1_hat_randoms,
            g1_polys, g1_poly_hats, g2_polys, g2_rho, g1_hat_rho):
    A = []
    B = []
    A_hat = []
    inverted_sigma = inverse_perm(sigma)
    for perm_i, g1_random, g1_hat_random, random, hat_random in zip(
            inverted_sigma,
            g1_randoms,
            g1_hat_randoms,
            randoms,
            hat_randoms):
        A.append(g1_polys[perm_i] + g1_random)
        B.append(g2_polys[perm_i] + random * g2_rho)
        A_hat.append(g1_poly_hats[perm_i] + hat_random * g1_hat_rho)

    return A, B, A_hat


def get_infs(gk):
    inf1 = G1Elem.inf(gk.G)
    inf2 = G2Elem.inf(gk.G)
    return inf1, inf2


def step_2(gk, A, B, g1_sum, g2_sum):
    inf1, inf2 = get_infs(gk)
    A.append(g1_sum - sum(A, inf1))
    B.append(g2_sum - sum(B, inf2))
    return A, B


def step_3(gk, A_hat, g1_hat_sum):
    inf1, inf2 = get_infs(gk)
    A_hat.append(g1_hat_sum - sum(A_hat, inf1))
    return A_hat


def step_4(gk, randoms, hat_randoms, g1_randoms, g1_rho):
    rand_n = - sum(randoms) % gk.q
    randoms.append(rand_n)
    hat_rand_n = - sum(hat_randoms) % gk.q
    hat_randoms.append(hat_rand_n)    
    g1_randoms.append(rand_n * g1_rho)
    return randoms, hat_randoms, g1_randoms


def step_5a(sigma, randoms, hat_randoms,
            g1_beta_polys,
            g1_beta_rhos, g1_beta_rhoshat):
    D = []
    inverted_sigma = inverse_perm(sigma)
    for perm_i, random, hat_random in zip(inverted_sigma, randoms, hat_randoms):
        D.append(g1_beta_polys[perm_i]
                 + random * g1_beta_rhos
                 + hat_random * g1_beta_rhoshat)
    return D


def step_5b(randoms, A, g1_randoms, sigma, g1_poly_zero, g1_poly_squares):
    C = []
    inverted_sigma = inverse_perm(sigma)
    for random, a, g1_random, perm_i in zip(
            randoms, A, g1_randoms, inverted_sigma):
        C.append(random * (2 * (a + g1_poly_zero) - g1_random) +
                 g1_poly_squares[perm_i])
    return C


def step_6(gk, t_randoms, g1_poly_hats, g1rhohat):
    rt = gk.q.random()
    inf1, _ = get_infs(gk)
    g1_t = rt * g1rhohat
    for t_random, g1_poly_hat in zip(t_randoms, g1_poly_hats):
        g1_t += t_random * g1_poly_hat
    return rt, g1_t


def step_7(gk, sigma, t_randoms, pk, ciphertexts):
    _, inf2 = get_infs(gk)
    M_primes = []
    for perm_i, t_random in zip(sigma, t_randoms):
        M_primes.append(tuple_add(ciphertexts[perm_i], enc(pk, t_random, 0)))
    return M_primes


def tuple_map(func, tpl):
    return tuple(map(func, tpl))


def tuple_add(tpl1, tpl2):
    zipped = zip(tpl1, tpl2)
    return tuple(z[0] + z[1] for z in zipped)


def step_8(B, C):
    return B[:-1], C


def step_9(pk, r_hat_t, randoms, ciphertexts):
    N = tuple_map(lambda elem: r_hat_t * elem, pk)
    for random, ciphertext in zip(randoms, ciphertexts):
        N = tuple_add(N, tuple_map(lambda elem: random * elem, ciphertext))
    return N


def step_10(D):
    return D


def step_11(A_hat, g1_t, N):
    return A_hat[:-1], g1_t, N


def step_12(M_primes, A, pi_1sp, pi_sm, pi_con):
    return M_primes, A[:-1], pi_1sp, pi_sm, pi_con


def prove(n, crs, ciphertexts, sigma, t_randoms):
    
    (randoms,
     g1_randoms,
     hat_randoms,
     g1_hat_randoms) = step_1a(n, crs.gk.q, crs.g1rho)
    A, B, A_hat = step_1b(
        sigma,
        randoms, g1_randoms,
        hat_randoms, g1_hat_randoms,
        crs.g1_polys, crs.crs_con.g1_poly_hats,
        crs.g2_polys, crs.g2rho, crs.crs_con.g1rhohat)
    A, B = step_2(crs.gk, A, B, crs.crs_1sp.g1_sum, crs.crs_1sp.g2_sum)
    A_hat = step_3(crs.gk, A_hat, crs.crs_1sp.g1_hat_sum)
    (randoms,
     hat_randoms,
     g1_randoms) = step_4(crs.gk,
                          randoms,
                          hat_randoms,
                          g1_randoms,
                          crs.g1rho)    
    D = step_5a(
        sigma,
        randoms,
        hat_randoms,
        crs.crs_sm.g1_beta_polys,
        crs.crs_sm.g1_beta_rhos,
        crs.crs_sm.g1_beta_rhoshat)
    C = step_5b(randoms, A, g1_randoms, sigma,
               crs.crs_1sp.g1_poly_zero, crs.crs_1sp.g1_poly_squares)    
    rt, g1_t = step_6(
        crs.gk, t_randoms, crs.crs_con.g1_poly_hats, crs.crs_con.g1rhohat)
    M_primes = step_7(crs.gk, sigma, t_randoms, crs.pk, ciphertexts)
    pi_1sp = step_8(B, C)    
    N = step_9(crs.pk, rt, hat_randoms, ciphertexts)
    pi_sm = step_10(D)
    pi_con = step_11(A_hat, g1_t, N)
    pi_sh = step_12(M_primes, A, pi_1sp, pi_sm, pi_con)
    return pi_sh

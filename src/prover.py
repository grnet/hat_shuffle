
def step1a(n, q, g1rho):
    randoms = [q.random() for i in range(n - 1)]
    g1_randoms = list(map(lambda random: random * g1rho, randoms))
    return randoms, g1_randoms


def step1b(sigma, randoms, g1_randoms,
           g1_polys, g1_poly_hats, g2_polys, g2rho, g1rhohat):
    A = []
    B = []
    A_hat = []
    for perm_i, g1_random, random in zip(sigma, g1_randoms, randoms):
        A.append(g1_polys[perm_i] + g1_random)
        B.append(g2_polys[perm_i] + random * g2rho)
        A_hat.append(g1_poly_hats[perm_i] + random * g1rhohat)

    return A, B, A_hat

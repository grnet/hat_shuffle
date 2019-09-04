from libffpy.libffpy import BigNum

def lagrangian(i, n, chi, q):
    """Evaluates Lagrange basis polynomial l_i at point x.

    Distinct points are 1, 2, ..., n + 1.
    Returns nonzero field element.

    Arguments:
    i -- polynomial index in range 1, 2, ..., n + 1
    chi -- input value of the polynomial
    q -- the order of the group
    """
    numerator = BigNum(1)
    denominator = BigNum(1)
    for j in range(1, n+2):
        if i == j:
            continue

        numerator *= chi - j
        elem = i - j
        denominator *= elem

    return numberator * denominator.mod_inverse()

def compute_denominators(k):
    """Computes denominators for Lagrange basis polynomials.

    Uses distinct points 1, ...,k
    Arguments:
    k -- number of basis polynomials
    q -- the order of the group
    """
    denominators = []
    temp = BigNum(1)
    for i in range(1, k+1):
        if i == 1:
            for j in range(2, k+1):
                elem = i - j;
                temp *= elem
        elif i == k:
            elem = 1 - k;
            temp *= elem
        else:
            inverse = BigNum(i - 1 - k)
            inverse = inverse.mod_inverse()
            elem = i - 1
            temp *= elem
            temp *= inverse
        denominators.append(temp)
    return denominators


def compute_denominators_slow(k):
    """Computes denominators for Lagrange basis polynomials.
    This function can be used to test compute_denominators(k, q).

    Uses distinct points 1, ...,k
    Arguments:
    k -- number of basis polynomials
    q -- the order of the group
    """
    denominators = []

    for i in range(1, k+1):
        denominator = BigNum(1)
        for j in range(1, k+1):
            if i == j:
                continue
            elem = i - j
            denominator *= elem
        denominators.append(denominator)
    return denominators


def generate_pis(chi, n):
    """Computes vector of elements P_i(chi) for i = 0, ..., n.

    P_0 is special, defined as ln_plus1(chi) - 1, where ln_plus1 is the
    (n+1)th Lagrange basis polynomial.
    The rest P_i are defined as 2*ln_i(ch) + ln_plus1(chi), where ln_i is the
    ith Lagrange basis polynomial.
    It returns a list with the values of the n+1 polynomials P_i(chi).
    Uses Lagrange basis polynomials with distinct points 1, ..., n + 1.
    Arguments:
    chi -- point of evaluation, must be a Bn
    n -- the number of elements, a Python integer
    q -- the order of the group, must be a Bn
    """

    #  if chi <= BigNum(n + 1):
        #  raise ValueError("chi should be greater than n + 1, chi=%s n+1=%s"
                         #  % (chi, n+1))
    pis = []

    prod = BigNum(1)
    for j in range(1, n + 2):
        prod *= (chi - j)

    # denoms[0] = 1 / (w_1 - w_2) (w_1 - w_3) ... (w_1 - w_{n + 1})
    # denoms[1] = 1 / (w_2 - w_1) (w_2 - w_3) ... (w_2 - w_{n + 1})
    # denoms[n] = 1 / (w_{n+1}- w_1) (w_{n+1} - w_2) ... (w_{n+1} - w_n)
    denoms = compute_denominators(n + 1)

    missing_factor = chi - (n + 1)

    ln_plus1 = prod * missing_factor.mod_inverse()
    ln_plus1 *= denoms[n].mod_inverse()

    # P_0 is special
    pis.append(ln_plus1 - BigNum(1))

    two = BigNum(2)
    for i in range(1, n + 1):
        missing_factor = chi - i
        l_i = prod * missing_factor.mod_inverse()
        l_i *= denoms[i - 1].mod_inverse()
        pis.append(two * l_i + ln_plus1)

    return pis

def generate_pi_hats(chi, n, q):
    """Computes vector of elements \hat{P}_i(chi) for i = 1, ..., n.

    These are simply the polynomials x^{(i+1)(n+1)}.
    It returns a list with the values of the n polynomials \hat{P}_i(chi).
    Arguments:
    chi -- point of evaluation, must be a Bn
    n -- the number of elements, a Python integer
    q -- the order of the group, must be a Bn
    """

    hpis = []
    hpi = chi**(n+1)
    hpis = [ hpi**(i+1) for i in range(1, n+1)]

    return hpis

def test_generate_pis():
    a = generate_pis(BigNum(6), 2, BigNum(7))
    assert(generate_pis(BigNum(6), 2, BigNum(7)) == [2, 1, 1])
    assert(generate_pis(BigNum(8), 3, BigNum(17)) == [0, 12, 5, 3])
    assert(generate_pis(BigNum(9), 4, BigNum(17)) == [1, 4, 5, 1, 13])


def test_generate_pi_hats():
    assert(generate_pi_hats(BigNum(6), 3, BigNum(997)) == [668, 332, 565])
    assert(generate_pi_hats(BigNum(6), 5, BigNum(997)) == [332, 400, 554, 199, 480])
    assert(generate_pi_hats(BigNum(17), 7, BigNum(313)) == [16, 249, 256, 228, 27,
                                                 205, 119])

if __name__ == '__main__':
    test_generate_pis()
    test_generate_pi_hats()

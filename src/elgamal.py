from libffpy import LibffPy


def gen_params_bp_g2(n):
    G = LibffPy(n)
    g = G.gen2()
    o = G.order()
    return (G, g, o)


def key_gen(params):
    _, g, o = params
    priv = o.random()
    pub = (g, priv * g)
    return (pub, priv)


def enc(pub, r, m):
    pk1, pk2 = pub
    a = r * pk1
    b = m * pk1 + r * pk2
    return (a, b)


def dec(priv, c, table):
    a, b = c
    v = b + (-priv * a)
    return table[v]


def make_table(g, n):
    table = {}
    for i in range(n):
        elem = (i * g)
        table[elem] = i
    return table


def test_encdec(params):
    table = make_table(params[1], 1000)
    G, g, o = params
    pub, priv = key_gen(params)
    g2 = G.gen2()
    import random
    ps = random.sample(range(1000), 100)
    for i in range(100):
        r = o.random()
        c = enc(pub, r, ps[i])
        assert(dec(priv, c, table) == ps[i])


if __name__ == '__main__':
    print("Testing BP group G2...")
    test_encdec(gen_params_bp_g2(100))

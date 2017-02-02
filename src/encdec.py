import elgamal


def encrypt(q, pk, m):
    s = q.random()
    return elgamal.enc(pk, s, m)


def make_table(pk, n):
    return elgamal.make_table(pk[0], n)


def decrypt(ctext, secret, table):
    return elgamal.dec(secret, ctext, table)

import random
import datetime
import sys

import crs
import encdec
import prover
import verifier_nb


system_random = random.SystemRandom()


def secure_shuffle(lst):
    random.shuffle(lst, random=system_random.random)


def random_permutation(n):
    s = list(range(n))
    secure_shuffle(s)
    return s


def initialize(n):
    gk = crs.mk_gk()
    Chi = crs.mk_Chi(gk.q)
    CRS, td = crs.mk_crs(n, gk, Chi)
    return gk, Chi, CRS


def mk_t_randoms(n, q):
    return [q.random() for i in range(n)]


def demo(n, messages):
    gk, Chi, CRS = initialize(n)
    secret = Chi.sk
    pk = CRS.pk
    ciphertexts = encrypt_messages(gk.q, pk, messages)

    start = datetime.datetime.now()
    sigma = random_permutation(n)
    print("SIGMA = %s" % sigma)
    t_randoms = mk_t_randoms(n, gk.q)
    pi_sh = prover.prove(n, CRS, ciphertexts, sigma, t_randoms)
    shuffled_ciphertexts, A, pi_1sp, pi_sm, pi_con = pi_sh
    perm_ok, sm_ok, cons_ok = verifier_nb.verify_batched(CRS, ciphertexts, pi_sh)
    print("VERIFY: %s %s %s" % (perm_ok, sm_ok, cons_ok))
    end = datetime.datetime.now()

    TABLE = encdec.make_table(pk, n)
    shuffled_ms = decrypt_messages(secret, TABLE, shuffled_ciphertexts)
    print(shuffled_ms)
    print("elapsed: %s" % (end - start))


def encrypt_messages(order, pk, messages):
    return [encdec.encrypt(order, pk, message) for message in messages]


def decrypt_messages(secret, table, ciphertexts):
    return [encdec.decrypt(cs, secret, table) for cs in ciphertexts]


if __name__ == '__main__':
    n = 10
    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
    messages = list(range(n))
    demo(len(messages), messages)

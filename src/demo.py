import random
import datetime
import argparse

import crs
import encdec
import prover
import verifier


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


def demo(n, messages, batch=True):
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
    verify = verifier.verify_batched if batch else verifier.verify_non_batched
    perm_ok, sm_ok, cons_ok = verify(n, CRS, ciphertexts, pi_sh)
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


DEFAULT_N = 10
parser = argparse.ArgumentParser(description='Hat shuffler')
parser.add_argument('n', metavar='N', type=int, nargs='?', default=DEFAULT_N,
                    help='number of messages')
parser.add_argument('--nb', action='store_true',
                    default=False,
                    help="Don't batch verification (default is batching)")


if __name__ == '__main__':
    args = parser.parse_args()
    messages = list(range(args.n))
    demo(len(messages), messages, batch=not args.nb)

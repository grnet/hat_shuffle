from cProfile import Profile
from pstats import Stats
import random
import datetime
import argparse

import src.crs as crs
import src.encdec as encdec
import src.prover as prover
import src.verifier as verifier


system_random = random.SystemRandom()


def secure_shuffle(lst):
    random.shuffle(lst, random=system_random.random)


def random_permutation(n):
    s = list(range(n))
    secure_shuffle(s)
    return s


def initialize(n):
    gk = crs.mk_gk(n)
    Chi = crs.mk_Chi(gk.q)
    CRS, td = crs.mk_crs(n, gk, Chi)
    return gk, Chi, CRS


def mk_t_randoms(n, q):
    return [q.random() for i in range(n)]


def demo(n, messages, batch=True):
    start = datetime.datetime.now()

    gk, Chi, CRS = initialize(n)

    time_init = datetime.datetime.now() - start
    print("Initialization: %s" % time_init)
    time_init = datetime.datetime.now()

    secret = Chi.sk
    pk = CRS.pk
    ciphertexts = encrypt_messages(gk.q, pk, messages)

    time_enc = datetime.datetime.now() - time_init
    print("Encryption: %s" % time_enc)
    time_enc = datetime.datetime.now()

    sigma = random_permutation(n)

    time_perm = datetime.datetime.now() - time_enc
    print("Random Permutations: %s" % time_perm)
    time_perm = datetime.datetime.now()

    #  print("SIGMA = %s" % sigma)
    t_randoms = mk_t_randoms(n, gk.q)
    pi_sh = prover.prove(n, CRS, ciphertexts, sigma, t_randoms)
    shuffled_ciphertexts, A, pi_1sp, pi_sm, pi_con = pi_sh

    time_proof = datetime.datetime.now() - time_perm
    print("Proof: %s" % time_proof)
    time_proof = datetime.datetime.now()

    verify = verifier.verify_batched if batch else verifier.verify_non_batched
    perm_ok, sm_ok, cons_ok = verify(n, CRS, ciphertexts, pi_sh)
    #  profiler = Profile()
    #  profiler.runctx('perm_ok, sm_ok, cons_ok = verify(n, CRS, ciphertexts,\
                    #  pi_sh)', {'verify': verify, 'n': n, 'CRS':
                                  #  CRS, 'ciphertexts': ciphertexts, 'pi_sh':
                              #  pi_sh}, {})
    #  stats = Stats(profiler)
    #  stats.sort_stats('cumulative')
    #  stats.print_stats()
    #  stats.print_callers()
    print("VERIFY: %s %s %s" % (perm_ok, sm_ok, cons_ok))

    time_ver = datetime.datetime.now() - time_proof
    print("Verification: %s" % time_ver)
    time_ver = datetime.datetime.now()

    TABLE = encdec.make_table(pk, n)
    shuffled_ms = decrypt_messages(secret, TABLE, shuffled_ciphertexts)

    time_dec = datetime.datetime.now() - time_ver
    print("Decryption: %s" % time_dec)
    #  print(shuffled_ms)

    end = datetime.datetime.now() - start
    print("Ellapsed: %s" % end)

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
    #  profiler = Profile()
    #  l = len(messages)
    #  profiler.runctx('demo(l, messages)', {'l': l, 'messages': messages, 'demo': demo}, {})
    #  stats = Stats(profiler)
    #  stats.sort_stats('cumulative')
    #  stats.print_stats()

Implementation of a Re-Encryption Mix-Net
======================================================

This module implements the re-encryption mix-net
presented by Fauzi et al. in their paper:
["An Efficient Pairing-Based Shuffle Argument
Draft"](http://kodu.ut.ee/~lipmaa/papers/flsz17/hat_shuffle.pdf).
We use the
[libffpy](https://github.com/eellak/gsoc17module-zeus/tree/master/libffpy)
wrapper of [libff](https://github.com/scipr-lab/libff) library
for multiplications on the elliptic curve.

Python
======

The module requires **Python 2.7**.

Installing libffpy
==================

```bash
sudo apt-get install build-essential git libboost-all-dev cmake libgmp3-dev libssl-dev libprocps4-dev pkg-config
pip install libffpy
```

***So far we have tested these only on Ubuntu 16.04 LTS.***

Usage
=====

There exists a demo in the file demo.py of the root directory
that shows the basic workflow of the mix-net module.

To run it:

```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprocps.so
cp libffpy/build/lib.linux-x86_64-2.7/libffpy.so  libffpy/libffpy.so
python demo.py
```

Or try:

```bash
./run.sh
```

Run with docker
===============

```bash
docker build -t hat_shuffle .
docker run -it hat_shuffle 5
```

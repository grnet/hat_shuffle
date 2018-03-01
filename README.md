Implementation of a Re-Encryption Mix-Net
======================================================

This module implements the re-encryption mix-net
presented by Fauzi et al. in their paper:
["An Efficient Pairing-Based Shuffle Argument
Draft"](http://kodu.ut.ee/~lipmaa/papers/flsz17/hat_shuffle.pdf).
We use the [libffpy](edit/master/REA…) wrapper of
[libff](https://github.com/scipr-lab/libff) library
for multiplications on the elliptic curve.

Python
======

The module requires **Python 2.7**.


Installing Dependencies
=======================

1. Install [libsnark](https://github.com/scipr-lab/libsnark) following
the instructions on its GitHub page.
	* Install libsnark on `/usr/` with
	```
	make install PREFIX=/usr
	```
	after compiling it.
2. Install [libff](https://github.com/scipr-lab/libff) following
the instructions on its GitHub page.
	* After installing libff, inside the cloned repo copy
	the third party libraries to the local includes.
	```
	cp -R depends /usr/local/include/
	```

   * Add to the libff library (before compiling it) the `-fPIC`
  	flag on CMakeLists. Specifically on the
  	`CMakeLists.txt` file add `-fPIC` to the existing flags on `CMAKE_CXX_FLAGS`
  	and `CMAKE_EXE_LINKER_FLAGS`.


    * In order to avoid libff outputting profiling info change the variables
  	`inhibit_profiling_info` and `inhibit_profiling_counters` to `true` on
  	`libff/common/profiling.cpp` before compiling the library.

3. Install [ate-pairing](https://github.com/herumi/ate-pairing) following
the instructions on its GitHub page (with SUPPORT_SNARK=1)
4. Install package dependencies
```
    sudo apt-get install python python-pip
```
5. Install Cython
```
    pip install cython
```

***So far we have tested these only on Ubuntu 16.04 LTS.***

Installing libffpy
==================

- Change the path of ate-pairing lib in line 21 of libffpy/setup.py.

```
sudo ./build.sh
```

Usage
=====

There exists a demo in the file demo.py of the root directory
that shows the basic workflow of the mix-net module.

To run it:

```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprocps.so
python demo.py
```

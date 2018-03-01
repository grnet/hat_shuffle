#!/bin/bash
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprocps.so
cd libffpy
rm -fr build/
rm libffpy.so
sudo python setup.py install &
wait
cp build/lib.linux-x86_64-2.7/libffpy.so  ./
python demo.py 10
# cd ../
# rm -fr build/
# sudo python setup.py install &
# wait
# python demo.py 10

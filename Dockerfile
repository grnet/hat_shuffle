FROM ubuntu:16.04

ENV HOME /root

# Install libsnark
RUN apt-get update && apt-get install -y \
    build-essential cmake git libgmp3-dev libprocps4-dev python-markdown \
    libboost-all-dev libssl-dev pkg-config vim

WORKDIR $HOME

RUN git clone https://github.com/vitsalis/libffpy.git
ENV LIBFFPY /root/libffpy
WORKDIR $LIBFFPY
RUN cd libffpy && git submodule init && git submodule update && \
    cd libff && git submodule init && git submodule update
WORKDIR $LIBFFPY
COPY helper/CMakeLists.txt libffpy/libff/CMakeLists.txt
RUN cd libffpy/libff && mkdir -p build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=../ && make && make install
WORKDIR $LIBFFPY

RUN apt-get install -y python python-pip && pip install cython

RUN python setup.py build_ext --inplace && python setup.py install

WORKDIR $HOME

RUN git clone https://github.com/grnet/hat_shuffle.git

WORKDIR hat_shuffle

RUN git fetch && git checkout libffpy

ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprocps.so

ENTRYPOINT ["python", "demo.py"]

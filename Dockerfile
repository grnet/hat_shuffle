FROM ubuntu:16.04
MAINTAINER Stefanos Chaliasos "schaliasos@grnet.gr"

ENV HOME /root

# Install libsnark
RUN apt-get update && apt-get install -y \
    build-essential cmake git libgmp3-dev libprocps4-dev python-markdown \
    libboost-all-dev libssl-dev pkg-config
RUN git clone https://github.com/scipr-lab/libsnark.git && cd libsnark && \
    git submodule init && git submodule update && mkdir build && cd build && \
    cmake .. && make && make install PREFIX=/usr

WORKDIR $HOME

RUN git clone git://github.com/grnet/hat_shuffle.git && cd hat_shuffle \
    && git fetch && git checkout docker

WORKDIR $HOME

# Install libff
RUN apt-get install -y libboost-all-dev libgmp3-dev
RUN git clone https://github.com/scipr-lab/libff.git && cd libff && git submodule init && \
    git submodule update && rm CMakeLists.txt && cp ../hat_shuffle/CMakeLists.txt ./ \
    && sed -i 's/bool inhibit_profiling_info = false;/bool inhibit_profiling_info = true;/g' libff/common/profiling.cpp \
    && sed -i 's/bool inhibit_profiling_counters = false;/bool inhibit_profiling_counters = true;/g' libff/common/profiling.cpp \
    && mkdir build && cd build && cmake .. && make && \
    make install && cd ../ && cp -R depends /usr/local/include/

WORKDIR $HOME

# Install ate-pairing
RUN git clone git://github.com/herumi/xbyak.git && \
    git clone git://github.com/herumi/ate-pairing.git && cd ate-pairing && \
    make -j SUPPORT_SNARK=1

WORKDIR $HOME

# Install dependecies
RUN apt-get install -y python python-pip && pip install cython
RUN cd hat_shuffle && ./build.sh
ENV LD_PRELOAD /usr/lib/x86_64-linux-gnu/libprocps.so

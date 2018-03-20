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

# Install libff
RUN apt-get install libboost-all-dev libgmp3-dev
RUN git clone https://github.com/scipr-lab/libff.git &&  cd libff && git submodule init && \
    git submodule update && mkdir build && cd build && cmake .. && make && \
    make install && cp -R depends /usr/local/include/

WORKDIR $HOME

# Install ate-pairing
RUN git clone git://github.com/herumi/xbyak.git && \
    git clone git://github.com/herumi/ate-pairing.git && cd ate-pairing && \
    make -j SUPPORT_SNARK=1

WORKDIR $HOME
RUN pwd

# Install dependecies
#RUN apt-get install python python-pip && pip install cython
#RUN git clone git@github.com:grnet/hat_shuffle.git && cd hat_shuffle && \
    # git checkout -b docker origin/docker && ./build

FROM ubuntu:16.04

ENV HOME /root

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

RUN apt-get install -y python3 python3-pip && pip3 install cython

RUN echo "" > libffpy/__init__.py

RUN python3 setup.py build_ext --inplace && python3 setup.py install

WORKDIR $HOME

RUN mkdir hat_shuffle

WORKDIR hat_shuffle

COPY src/ src
COPY demo.py ./

ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libprocps.so

ENTRYPOINT ["python3", "demo.py"]

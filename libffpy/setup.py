import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

from Cython.Distutils import build_ext


os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

setup(
    name='libffpy',
    ext_modules=cythonize(
        Extension(
            "libffpy",
            sources=["libffpy.pyx", "libff_wrapper.cpp"],
            language="c++",
            include_dirs=["libff/include", "libff"],
            library_dirs = ["/usr/local/lib", "libff/lib", "libff/build/depends"],
            extra_compile_args = ["-std=c++11", "-fPIC", "-shared", "-w", "-static", "-O3"],
            extra_link_args = ["-lgmp", "-lzm", "-lff", "-fopenmp", "-g"]
        )
    ),
    cmdclass = {'build_ext': build_ext},
    setup_requires=[
        "cython >= 0.22.1",
    ],
    install_requires=[
	"cython >= 0.22.1",
    ]
)

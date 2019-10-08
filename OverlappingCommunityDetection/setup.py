#from distutils.core import setup, Extension
#import numpy
#from Cython.Build import cythonize
#
#setup(ext_modules = cythonize(Extension(
#           "pprgrow_cy.pyx",                 # our Cython source
#           sources=["pprgrow_min_cond.cpp"],
#           language="c++",             # generate C++ code
#           extra_compile_args=['-std=c++11']
#      )))

from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_cond",
                 sources=["_pprgrow_cy_cond.pyx", "pprgrow_min_cond.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)

'''setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_ceil",
                 sources=["_pprgrow_cy_ceil.pyx", "pprgrow_max_ceil.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_mceil",
                 sources=["_pprgrow_cy_mceil.pyx", "pprgrow_max_mceil.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_ccnes",
                 sources=["_pprgrow_cy_ccnes.pyx", "pprgrow_max_ccnes.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_tpr",
                 sources=["_pprgrow_cy_tpr.pyx", "pprgrow_max_tpr.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_fomd",
                 sources=["_pprgrow_cy_fomd.pyx", "pprgrow_max_fomd.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)'''

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("pprgrow_cy_mod",
                 sources=["_pprgrow_cy_mod.pyx", "pprgrow_max_mod.cpp"],
                 language="c++",
                 extra_compile_args=["-std=c++11"],
                 include_dirs=[numpy.get_include()])],
)


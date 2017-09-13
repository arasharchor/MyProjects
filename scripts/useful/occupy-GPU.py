import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import numpy
a = numpy.random.randn(40000,40000)

a = a.astype(numpy.float32)

a_gpu = cuda.mem_alloc(a.nbytes)


cuda.memcpy_htod(a_gpu, a)



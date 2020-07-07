from theano.tensor.nnet.tests import test_neighbours

from .config import mode_with_gpu

from ..neighbours import GpuImages2Neibs


class TestGpuImages2Neibs(test_neighbours.TestImages2Neibs):
    mode = mode_with_gpu
    op = GpuImages2Neibs
    dtypes = ["int64", "float32", "float64"]

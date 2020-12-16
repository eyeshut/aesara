from copy import copy

from theano.gof import utils
from theano.gof.utils import undef


class Linker:
    """
    WRITEME

    """

    def clone(self, allow_gc=undef):
        new = copy(self)
        if allow_gc is not undef:
            new.allow_gc = allow_gc
        return new

    def make_thunk(self):
        """
        This function must return a triplet (function, input_variables,
        output_variables) where function is a thunk that operates on the
        returned variables. If inplace is True, the input_variables and
        output_variables lists will be the same as the inputs and outputs
        of the graph provided to the L{Linker}. Else, independent
        variables will be returned.

        Examples
        --------
        x, y = Variable(Double), Variable(Double)
        e = x + y
        fgraph = FunctionGraph([x, y], [e])
        fn, (new_x, new_y), (new_e, ) = MyLinker(fgraph).make_thunk(inplace)
        new_x.data = 1.0
        new_y.data = 2.0
        fn()
        print new_e.data # 3.0
        print e.data # 3.0 iff inplace == True (else unknown)

        """
        raise utils.MethodNotDefined("make_thunk", type(self), self.__class__.__name__)

    # DELETEME #
    def make_function(self, unpack_single=True, **kwargs):
        """
        Returns a function that takes values corresponding to the inputs of the
        fgraph used by this L{Linker} and returns values corresponding the the
        outputs of that fgraph. If inplace is True, the calculations will
        operate in the same storage the fgraph uses, else independent storage
        will be allocated for the function.

        Examples
        --------
        e = x + y
        fgraph = FunctionGraph([x, y], [e])
        fn = MyLinker(fgraph).make_function(inplace)
        print fn(1.0, 2.0) # 3.0
        print e.data # 3.0 iff inplace == True (else unknown)

        If unpack_single is True (default) and that the function has only one
        output, then that output will be returned. Else, a list or tuple of
        length 1 will be returned.

        """
        thunk, inputs, outputs = self.make_thunk(**kwargs)

        def execute(*args):
            def e_arity(takes, got):
                return f"Function call takes exactly {takes} {['argument', 'arguments'][takes > 1]} ({got} given)"

            if len(args) != len(inputs):
                raise TypeError(e_arity(len(inputs), len(args)))
            for arg, variable in zip(args, inputs):
                variable.data = arg
            thunk()
            if unpack_single:
                return utils.to_return_values([variable.data for variable in outputs])
            else:
                return [variable.data for variable in outputs]

        execute.thunk = thunk
        execute.inputs = inputs
        execute.outputs = outputs

        return execute

    def schedule(self, fgraph):
        return fgraph.toposort()

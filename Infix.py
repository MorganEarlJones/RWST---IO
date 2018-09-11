#The following code is a popular hack that allows custom infix operators
#see http://code.activestate.com/recipes/384122-infix-operators/
from functools import partial
class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

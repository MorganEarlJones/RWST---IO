from Infix import Infix

import time
import os


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

"""
the following classes represent the primitives of the IO monad
"""

class Pure:
  def __init__(self,val):
    self.val = val
  def bind(self,k):
    return k(self.val)
  def iBind(self,k):
    return k(*(self.val))
  def eval(self):
    return self

class GetLine:
  def __init__(self):
    self.val = ()
  def bind(self,k):
    self.val = input('')
    return k(self.val)
  def iBind(self,k):
    self.val = input('')
    return k(*self.val)

class Print:
  def __init__(self,str_):
    self.str = str_
  def bind(self,k):
    print(self.str)
    return k(())
  def iBind(self,k):
    print(self.str)
    return k(*())

class Clear:
  def __init__(self):
    self.val = ()
  def bind(self,k):
    cls()
    return k(())
  def iBind(self,k):
    cls()
    return k(*())

class Wait:
  def __init__(self,time):
    self.val = ()
    self.time = time
  def bind(self,k):
    time.sleep(self.time)
    return k(())
  def iBind(self,k):
    time.sleep(self.time)
    return k(*())


Monad = {
  'pure' : lambda x: Pure(x),
  'bind' : lambda mx: lambda k: mx.bind(k),
  'iBind' : lambda mx: lambda k: mx.iBind(k)
}
runIO = lambda mx: mx.bind(Pure)

"""
forMIO is preferable to the previously defined forM when the nested
computation consists solely of IO as the former isn't stack safe.
"""
def forM(ls):
  def forM_(k):
    acc = Pure(())
    for i in ls:
      acc = acc.bind(lambda _: k(i))
    return acc
  return forM_

@Infix
def bind(mx,k):
  return mx.bind(k)
@Infix
def seq(mx,my):
  return mx.bind(lambda _: my)
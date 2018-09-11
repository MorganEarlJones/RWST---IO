from HelperFunctions import lcompose
import RWST
import IO

"""
This experiment supplements typeclasses with a dict-passing style;
I think that's the point of the "Scrap your typeclasses" blog post by
Gabriel Gonzalez, but I've only skimmed through it enough to get this
idea.

You'll find some function names(iPipe, iBind) begin with the letter 'i'.
This is to distinguish variations of functions that can pipe tuples into 
lambdas which take multiple arguments. These functions usually vary from
their single-argument counterparts with the use of the * prefix, e.g.,
from f(x) to f(*x), which, given an iterable value 'x' will pass the
elements of x as individual arguments of some multi-argument (but uncurried)
function 'f'.

It's important to note that with the exception of IO, no types are
explicitly defined here, but rather their shape is reflected in the
behavior of the functions that use them.
"""
"""Example code at bottom"""

stringMonoid = {
  'empty': '',
  'append' : lambda x: lambda y: x + y
}

#runRWSIO :: RWST r w s IO a -> IO a
runRWSIO = lambda mx: mx(IO.Monad)

pureIO = RWST.lift |lcompose| IO.Pure
getLineIO = RWST.lift(IO.GetLine())
printIO = RWST.lift |lcompose| IO.Print
clearIO = RWST.lift(IO.Clear())
waitIO = RWST.lift |lcompose| IO.Wait

thingo = RWST.forM(range(1,4))(lambda _:
  printIO("banana") |RWST.seq|
  waitIO(0.2)
  )

def fizzBuzz():
  IO.runIO(
    IO.Clear() |IO.seq|
    IO.Print("How many fizz would you like to buzz?") |IO.seq|
    IO.GetLine() |IO.bind| (lambda n: # n <- getLine
    IO.forM(range(1,int(n) + 1))(lambda i: # for i in range(1,n + 1)
      IO.Wait(0.01) |IO.seq|
      IO.Print(
        "FizzBuzz!" if i % 15 == 0
        else "Buzz!" if i % 5 == 0
        else "Fizz!" if i % 3 == 0
        else str(i)
    )) |IO.seq|
    IO.Wait(1.5) |IO.seq|
    IO.Clear() |IO.seq|
    IO.Print("yea ok buhbye!") |IO.seq|
    IO.Wait(1) |IO.seq|
    IO.Clear()
  )
  )


runRWSIO(thingo)(stringMonoid)(())(())
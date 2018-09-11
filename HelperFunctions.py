from Infix import Infix

"""
pipe is an operator for forward function application, a la Elixir, F# and Elm.
Can be used to make any multi-argument (curried) function an infix
operator in a pinch:

x |pipe| fun (y) = x `fun` y

Piping a variable through a clean chain of functions can give
a very clean notion of the flow of data, e.g., (using |> as |pipe|):

value
  |> f
  |> g y
  |> h 30 "banana"
  |> etc

Alternatively, you can pipe a value into a lambda to bind a given
transformation of the initial value scope for an imperative style,
e.g.,(where (λvar -> expr) is equivalent to (lambda var: expr)):

value
  |> f
  |> map g
  |> (λx -> x
  |> h 30 (x ++ " banana!")
  |> 
  )

x is called immediately to be piped through on the next line so
that, while the result of map g is bound to x, the flow of data
through the functions is uninterupted.

here's a example expression using all of these concepts:

[1..100] -- basically range(1,101)
  |> map (* 2) -- think of that as '|> map (λx -> x * 2)'
  |> andThen (λx -> x
  |> show -- basically the str function
  |> (++ " banana, ") -- |> (λstr -> str ++ " banana, ")
  )

which gives "2 banana, 4 banana, 6 banana, 8 banana ..."
if you're not familiar with the functions used, map is the
only member function of the Functor class, which applies
a function of some type 'a' to some type 'b' over the
parameterized 'carrier' type of the Functor. In this case,
the carrier type is Int, and the function is Int -> Int
being mapped over a list(the Functor) of Ints. This pattern
can extend to any type where some carrier type is parameterized,
such as a 'tree of some type 'a'', or even a function from
some type 'b' to some type 'a', where you'd map over the
return value of the function(but not the argument, as that
would require use of contramap, which I will not explain here).

andThen is the bind function or >>= operator of the Monad class,
and acts in this context as a smart pipe(the usefulness of this
metaphor is short-lived). andThen is the flipped version of
>>=, so it can be used with |>, which keeps the operator soup
to a minimum, but I will try to explain this pattern in terms
of the >>= operator, where x |> andThen f = x >>= f = bind x f.
>>= takes on the left some monadic value 'm of a', or just 'm a',
and pipes the 'a' through the function on the right, which is
a function from type 'a' to 'm b'. In this case, 'm' stands
for List, 'a' stands for Int, and 'b' stands for Char, so
we're piping a List of Ints through a function from Int to
a List of Chars(which is a String), if we were to use map
for this, we'd get back a List of Lists of Chars,
or to review, m a -> (a -> m b) -> m (m b), but with
a proper implementation of >>=, we want to boil down
that return value to just 'm b' so that
(>>=) :: m a -> (a -> m b) -> m b. The function used
to boil our List of List of Chars down to a List of Chars
is append(folded over the top level list), but generalized
accross all monads 'm', we call this function join.

show is a function which converts values to a String
where applicable, so basically the str function in Python.

"""

@Infix
def pipe(x,f):
  return f(x)
#iterable pipe operator, mostly for piping tuples into lambdas with
#multiple arguments for pattern matching
@Infix
def iPipe(x,f):
  return f(*x)
#function composition operator
@Infix
def lcompose(f,g):
    return (lambda x: f(g(x)))
#flipped function composition operator
@Infix
def rcompose(g,f):
    return (lambda x: f(g(x)))

flip = lambda f: lambda y: lambda x: f(x)(y)
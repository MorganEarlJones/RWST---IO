from Infix import Infix
from HelperFunctions import pipe

#type RWST r w s m a = Monad m -> Monoid w -> r -> s -> m (a,s,w)

Monad = {
  'pure' : lambda x: lambda monad: lambda monoid: lambda reader: lambda state:(
    monad['pure']((x,state,monoid['empty']))
  ),
  'bind' : lambda mmx: lambda k: lambda monad: lambda monoid: lambda reader: lambda state:(
    mmx(monad)(monoid)(reader)(state) |pipe| (lambda mx:
    monad['iBind'](mx)(lambda x,st,w:
    monad['iBind'](k(x)(monad)(monoid)(reader)(st))(lambda y,s,w_:
    monad['pure']((y,s,monoid['append'](w)(w_)))
    )))
  ),
  'iBind' : lambda mmx: lambda k: lambda monad: lambda monoid: lambda reader: lambda state:(
    mmx(monad)(monoid)(reader)(state) |pipe| (lambda mx:
    monad['iBind'](mx)(lambda x,st,w:
    monad['iBind'](k(*x)(monad)(monoid)(reader)(st))(lambda y,s,w_:
    monad['pure']((y,s,monoid['append'](w)(w_)))
    )))
  )
}

andThen = lambda k: lambda mx: Monad['bind'](mx)(k)
pure = lambda x: Monad['pure'](x)

#lift :: m a -> Monad m -> Monoid w -> RWST r w s m a
lift = (
  lambda m: lambda monad: lambda monoid: lambda _: lambda s:
  monad['bind'](m)(lambda x:
  monad['pure']((x,s,monoid['empty']))
  )
)
@Infix
def bind(mx,k):
    return andThen(k)(mx)
@Infix
def seq(mx,my):
  return andThen(lambda _: my)(mx)

def forM(ls):
  def forM_(k):
    acc = pure(())
    for i in ls:
      acc = acc |seq| k(i)
    return acc
  return forM_






#reader operations
reader = lambda f:(
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['pure']((f(r),s,monoid['empty']))
)

ask = lambda monad: lambda monoid: lambda r: lambda s: monad['pure']((r,s,monoid['empty']))

local = lambda f: lambda rwst:(
  lambda monad: lambda monoid: lambda r: lambda s: rwst(monad)(monoid)(f(r))(s)
)

asks = reader

#writer operations
writer = lambda a,w:(
  lambda monad: lambda monoid: lambda r: lambda s: monad['pure']((a,s,w))
)

tell = lambda w:(
  lambda monad: lambda monoid: lambda r: lambda s: monad['pure'](((),s,w))
)

listen = lambda rwst:(
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['iBind'](rwst(monad)(monoid)(r)(s))(lambda a,s_,w:
    monad['pure'](((a,w),s_,w))
  )
)

listens = (
  lambda f: lambda rwst:
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['iBind'](rwst(monad)(monoid)(r)(s))(lambda a,s_,w:
    monad['pure'](((a,f(w)),s_,w))
    )
)

#state operations
state = (
  lambda st:
  lambda monad: lambda monoid: lambda r: lambda s:
    st(s) |iPipe| (lambda a,s:
    monad['pure']((a,s,monoid['empty']))
    )
)
get = (
  lambda monad: lambda monoid: lambda r: lambda s:
  monad['pure']((s,s,monoid['empty']))
)
put = (
  lambda x:
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['pure'](((),x,monoid['empty']))
)
modify = (
  lambda f:
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['pure'](((),f(s),monoid['empty']))
)
gets = (
  lambda f:
  lambda monad: lambda monoid: lambda r: lambda s:
    monad['pure']((f(s),s,monoid['empty']))
)
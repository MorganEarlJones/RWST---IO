# the following functions give you Functor and Applicative functions for any Monad
applicativeFromMonad = lambda monad: {
  'pure' : monad['pure'],
  'apply' : lambda ff: lambda fx:
  monad['bind'](ff)(lambda f:
  monad['bind'](fx)(lambda x:
  monad['pure'](f(x))
  )),
  'iApply' : lambda ff: lambda fx:
  monad['bind'](ff)(lambda f:
  monad['bind'](fx)(lambda x:
  monad['pure'](f(*x))
  ))
}

functorFromApplicative = lambda applicative:{
  'map' : lambda f: lambda fx: applicative['apply'](applicative['pure'](f))(fx),
  'iMap' : lambda f: lambda fx: applicative['iApply'](applicative['pure'](f))(fx),
}

functorFromMonad = lambda monad: functorFromApplicative(applicativeFromMonad(monad))

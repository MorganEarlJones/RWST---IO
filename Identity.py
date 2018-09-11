#type Identity a = a
identityMonad = {
  'pure' : lambda x: x,
  'bind' : lambda mx: lambda k: k(mx),
  'iBind' : lambda mx: lambda k: k(*mx)
}
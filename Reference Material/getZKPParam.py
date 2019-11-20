import random

_mrpt_num_trials = 5 # number of bases to test

def is_probable_prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n is definitely composite

    for i in range(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True # no base tested showed n as composite

# Sole parameter to change: bits of security
k = 7

def findGeneratorForSafePrime(p):
  completed = False
  while not completed:
    alpha = random.randrange(p-1)
    for exp in [2, q]:
      b = pow(alpha,(p-1)//exp, p)
      tmp = b % p == 1
      if tmp: break
    if not tmp: completed = True
  return alpha

def getCircularGroup(g, p):
  group_elems = []
  for k in range(p-1):
      tmp = pow(g,k,p) #g**n % p
      group_elems.append(tmp)
  return group_elems

while True:
  q = 2*random.getrandbits(k-1)+1
  if not is_probable_prime(q): continue

  p = 2*q+1
  if not is_probable_prime(p): continue
  print(f'{p} is a probable safe prime')
  break

generator = findGeneratorForSafePrime(p)
print(f'{generator} is generator of Zp with p == {p} and q == {q}')
if k < 20:
  group_elements = getCircularGroup(generator, p)
  assert len(set(group_elements)) == len(group_elements)
  print(f'The group is of size p-1 == {len(set(group_elements))}')
  print(group_elements)

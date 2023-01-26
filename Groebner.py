from random import randint

from fields import Rational, FpFactory
from polynomials import PolynomialFactory
from ordering import totlex, totrevlex

# (a_i) >> (b_i)  <---->  a_i >= b_i for all i
def dominates(a, b):
    for i in range(0, len(a)):
        if a[i] < b[i]:
            return False
    return True

# (a_i), (b_i) ---> (max(a_i, b_i))
def monoLcm(a, b):
    return tuple(max(a[i], b[i]) for i in range(0, len(a)))

# (m_i), (a_i) ---> (m_i - a_i)
def coDeg(m, a):
    return tuple((m[i] - a[i]) for i in range(0, len(a)))

# deg of leading term
def degLt(poly, order):
    assert poly != type(poly).zero()
    
    keys = list(poly.info.keys())
    keys.sort(key=order)
    return keys[0]

# degree-to-term trans
def deg2term(deg, Poly):
    ret = Poly.one()
    for i in range(0, len(deg)):
        ret = ret * (Poly.indet(i) ** deg[i])
    return ret

# S-polynomial
def Spoly(f, g, order):
    Poly = type(f)
    
    a = degLt(f, order)
    b = degLt(g, order)
    m = monoLcm(a, b)

    A = deg2term(coDeg(m, a), Poly)
    B = deg2term(coDeg(m, b), Poly)

    S = A * f - B * g
    return S

# remainder of the generalized division algorithm
def genRem(f, gs, order):
    Poly = type(f)
    if f == Poly.zero():
        return Poly.zero()

    while True:
        if f == Poly.zero():
            break

        stop = True

        keys = list(f.info.keys())
        keys.sort(key=order)
        deg = keys[0]
        
        for gi in gs:
            degi = degLt(gi, order)
            
            if dominates(deg, degi):
                stop = False
                coeff = f.info[deg]
                coeffi = gi.info[degi]
                quo = Poly.const(coeff / coeffi) * deg2term(coDeg(deg, degi), Poly)
                f = f - quo * gi
                break
                
        if stop:
            break
    
    return f


# Buchberger's algorithm to obtain a Groebner basis,
def getGroeb(gens, order):
    if not gens:
        return []

    Poly = type(gens[0])

    # remove zero polys
    gens0 = []
    for gen in gens:
        if gen != Poly.zero():
            gens0.append(gen)
    gens = gens0

    checked = set()

    while True:
        again = False
        toAdd = None

        for i in reversed(range(0, len(gens))):
            for j in reversed(range(i + 1, len(gens))):
                if (i, j) in checked:
                    continue
                
                checked.add((i, j))
                S = Spoly(gens[i], gens[j], order)
                rem = genRem(S, gens, order)
                if rem != Poly.zero():
                    again = True
                    toAdd = rem
                    break
            
            if again:
                break
        
        if again:
            gens.append(toAdd)
        else:
            break
    

    # remove redundants
    while True:
        again = False
        domination = None

        for i in range(0, len(gens)):
            a = degLt(gens[i], order)

            for j in range(0, len(gens)):
                if j == i:
                    continue

                b = degLt(gens[j], order)
                if dominates(a, b):
                    again = True
                    domination = (i, j)

        if again:
            i, _ = domination
            del gens[i]
        else:
            break

    return gens
    
# given a polynomial f & Groebner basis of an ideal I,
# check whether f is in I
def checkMem(f, basis, order):
    return genRem(f, basis, order) == type(f).zero()


# generate random polynomial (only for tests)
def getRandPoly0(numVar, field, Poly):
    def getRandPoly():
        numMono = randint(1, 3)
        ret = Poly.zero()

        for _ in range(0, numMono):
            deg = []
            for _ in range(0, numVar):
                deg.append(randint(0, 3))
            deg = tuple(deg)

            N = randint(1, 100)
            mono = Poly({deg : field.one()}) * Poly.times(N)
            ret = ret + mono

        return ret
    return getRandPoly



# test
# *** CAUTION
# the processing time might be very long
# if it stucks ---> put a keyboard interrupt and try it again
# if the "bad init" message comes out ---> the ideal to test contains 1, so try it again
if __name__ == "__main__":
    tested = 0
    
    numExceptions = 0

    for field in [Rational, FpFactory(71), FpFactory(839)]:
        for numVar in [2]:
            Poly = PolynomialFactory(numVar, field)

            getRandPoly = getRandPoly0(numVar, field, Poly)

            gens = [getRandPoly() for _ in range(0, randint(3, 6))]

            numExp = 3
            expPos = []
            for _ in range(0, numExp):
                f = Poly.zero()
                for gen in gens:
                    f = f + gen * getRandPoly()
                expPos.append(f)


            for order in [totrevlex, totlex]:
                basis = getGroeb(gens, order)

                if checkMem(Poly.one(), basis, order):
                    print("*** bad random init: ideal contains all. try it again.")
                    assert False

                for f in expPos:
                    if not checkMem(f, basis, order):
                        print(f)
                        print(basis)
                    assert checkMem(f, basis, order)
                    assert not checkMem(f + Poly.one(), basis, order)
                    tested += 1

    print("tested : " + str(tested))



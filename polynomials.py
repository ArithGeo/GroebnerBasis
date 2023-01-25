from fields import Field, Rational, FpFactory
from ordering import lex

def PolynomialFactory(numVar, baseField):
    assert issubclass(baseField, Field)
    assert numVar <= 5  # max: a,b,c,d,e

    class Polynomial:
        # basic
        def __init__(self, info):
            deepCopy = {}
            for deg, coeff in info.items():
                assert len(deg) == numVar
                assert type(coeff) == baseField
                for i in deg:
                    assert i >= 0

                deepCopy[deg] = coeff
            self.info = deepCopy
        
        def __eq__(self, B):
            if len(self.info) != len(B.info):
                return False
            else:
                for deg, coeff in self.info.items():
                    if not deg in B.info.keys():
                        return False
                    elif coeff != B.info[deg]:
                        return False
                return True

        def __str__(self): # always print in lex
            ret = ""
            vars = ["a", "b", "c", "d", "e"]
            sep = "  +  "

            keys = list(self.info.keys())
            keys.sort(key = lex)
            for key in keys:
                ret += f"{str(self.info[key])} "
                for i in range(0, numVar):
                    ret += f"{vars[i]}^{key[i]} "
                ret += sep
            ret = ret[ : -len(sep)]

            return ret

        # ring operations
        def __add__(self, B):
            info = {}
            for deg, coeff in self.info.items():
                info[deg] = coeff
            
            for deg, coeff in B.info.items():
                if deg in info.keys():
                    if info[deg] + coeff == baseField.zero():
                        del info[deg]
                    else:
                        info[deg] = info[deg] + coeff
                else:
                    info[deg] = coeff
            
            return Polynomial(info)

        def __neg__(self):
            info = {}
            for deg, coeff in self.info.items():
                info[deg] = -coeff
            return Polynomial(info)    

        def zero():
            return Polynomial({})

        def __mul__(self, B):
            info = {}
            for deg0, coeff0 in self.info.items():
                for deg1, coeff1 in B.info.items():
                    deg = tuple((deg0[i] + deg1[i]) for i in range(0, numVar))
                    coeff = coeff0 * coeff1

                    if not deg in info.keys():
                        info[deg] = baseField.zero()
                    info[deg] = info[deg] + coeff
            
            info1 = {}
            for deg, coeff in info.items():
                if info[deg] != baseField.zero():
                    info1[deg] = info[deg]
            return Polynomial(info1)

        def one():
            return Polynomial({tuple([0] * numVar) : baseField.one()})
        
        # useful APIs
        def times(N):
            ret = Polynomial.zero()
            for _ in range(0, N):
                ret = ret + Polynomial.one()
            return ret

        def const(k):
            return Polynomial({tuple([0] * numVar) : k})

        def indet(i): # gives i-th indeterminant
            assert i < numVar
            deg = [0] * numVar
            deg[i] = 1
            return Polynomial({tuple(deg) : baseField.one()})

        def __sub__(self, B):
            return self + (-B)

        def __pow__(self, N):
            ret = type(self).one()
            for _ in range(0, N):
                ret = ret * self
            return ret

    return Polynomial


# test
if __name__ == "__main__":
    tested = 0

    # check identity (a^3 + b^3 + c^3 - 3abc) = (a + b + c)(a^2 + b^2 + c^2 - ab - bc - ca)  
    fields = [Rational, FpFactory(2), FpFactory(3), FpFactory(5)]
    for field in fields:
        Polynomial = PolynomialFactory(3, field)
        a = Polynomial.indet(0)
        b = Polynomial.indet(1)
        c = Polynomial.indet(2)

        f = a + b + c
        g = (a ** 2) + (b ** 2) + (c ** 2) - (a * b) - (b * c) - (c * a)
        h = (a ** 3) + (b ** 3) + (c ** 3) - Polynomial.times(3) * (a * b * c)

        assert f * g == h
        tested += 1

        # reality check
        if False:
            print(f * g)

    print("tested : " + str(tested))



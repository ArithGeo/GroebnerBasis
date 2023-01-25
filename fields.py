from integers import gcd, invModPrime

class Field:
    # basic
    def __init__(self):
        pass # TODO
    
    def __eq__(self, B):
        pass # TODO

    def __str__(self):
        pass # TODO

    # getters
    # TODO

    # field operations
    def __add__(self, B):
        pass # TODO

    def __neg__(self):
        pass # TODO

    def zero():
        pass # TODO

    def __mul__(self, B):
        pass # TODO

    def one():
        pass # TODO

    def __invert__(self):
        pass # TODO

    # automatically defined
    def __sub__(self, B):
        return self + (-B)

    def __truediv__(self, B):
        return self * (~B)

    def __pow__(self, N):
        ret = type(self).one()
        for _ in range(0, N):
            ret = ret * self
        return ret


class Rational(Field):
    # basic
    def __init__(self, num, dom):
        assert dom != 0
        self.__num = num # numerator
        self.__dom = dom # dominator
    
    def __eq__(self, B):
        return (self.getNum() * B.getDom() == self.getDom() * B.getNum())

    def __str__(self):
        if self.getNum() == 0:
            return f"(+{0}/{1})"
        else:
            g = gcd(self.getNum(), self.getDom())
            a = abs(self.getNum()) // g
            b = abs(self.getDom()) // g

            if self.getNum() * self.getDom() > 0:
                return f"(+{a}/{b})"
            else:
                return f"(-{a}/{b})"

    # getters
    def getNum(self):
        return self.__num
    def getDom(self):
        return self.__dom

    # field operations
    def __add__(self, B):
        return Rational(
            self.getNum() * B.getDom() + self.getDom() * B.getNum(),
            self.getDom() * B.getDom()
        )

    def __neg__(self):
        return Rational(-self.getNum(), self.getDom())

    def zero():
        return Rational(0, 1)

    def __mul__(self, B):
        return Rational(
            self.getNum() * B.getNum(),
            self.getDom() * B.getDom()
        )

    def one():
        return Rational(1, 1)

    def __invert__(self):
        assert self.getNum() != 0
        return Rational(self.getDom(), self.getNum())


def FpFactory(p):
    class Fp(Field):
        # basic
        def __init__(self, rep):
            self.__rep = rep # representative
        
        def __eq__(self, B):
            return (self.getRep() % p == B.getRep() % p)

        def __str__(self):
            return f"({self.getRep() % p})"

        # getters
        def getRep(self):
            return self.__rep

        # field operations
        def __add__(self, B):
            return Fp(self.getRep() + B.getRep())

        def __neg__(self):
            return Fp(-self.getRep())

        def zero():
            return Fp(0)

        def __mul__(self, B):
            return Fp(self.getRep() * B.getRep())

        def one():
            return Fp(1)

        def __invert__(self):
            assert self.getRep() % p != 0
            return Fp(invModPrime(self.getRep(), p))

    return Fp


# test
if __name__ == "__main__":
    tested = 0

    # check identity
    # x^3 + 1 = (x^2 - x + 1) * (x + 1)

    for a in range(-30, +30):
        for b in range(-30, +30):
            if b == 0:
                continue
            x = Rational(a, b)
            assert (x ** 3) + Rational.one() == ((x ** 2) - x + Rational.one()) * (x + Rational.one())
            tested += 1

    # Frobenius automorphism
    # x^p = x
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        Fp = FpFactory(p)
        for a in range(-30, +30):
            x = Fp(a)
            (x ** p) == x
            tested += 1

    print("tested : " + str(tested))


from functools import cmp_to_key

# lexicographical monomial order
def lex0(a, b):
    for i in range(0, len(a)):
        if a[i] < b[i]:
            return +1
        elif a[i] > b[i]:
            return -1
    return 0

def lex1(a, b, tot=False):
    if tot:
        if sum(a) < sum(b):
            return +1
        elif sum(a) > sum(b):
            return -1
    return lex0(a, b)
        

# lexicographical monomial order with 2 options
# tot=True --> graded
# rev=True --> reversed
def lexOpt(a, b, tot=False, rev=False):
    if rev:
        return lex1(a[len(a)-1::-1], b[len(b)-1::-1], tot)
    else:
        return lex1(a, b, tot)

# 4 monomial ordering
lex = cmp_to_key(lambda a, b: lexOpt(a, b, False, False))
revlex = cmp_to_key(lambda a, b: lexOpt(a, b, False, True))
totlex = cmp_to_key(lambda a, b: lexOpt(a, b, True, False))
totrevlex = cmp_to_key(lambda a, b: lexOpt(a, b, True, True))


# test
if __name__ == "__main__":
    tested = 0

    monos = []
    for a in range(0, +10):
        for b in range(0, +10):
            for c in range(0, +10):
                monos.append((a, b, c))
    
    monos.sort(key = revlex)
    i = 0
    for c in reversed(range(0, +10)):
        for b in reversed(range(0, +10)):
            for a in reversed(range(0, +10)):
                assert monos[i] == (a, b, c)
                i += 1
                tested += 1

    monos.sort(key = lex)
    i = 0
    for a in reversed(range(0, +10)):
        for b in reversed(range(0, +10)):
            for c in reversed(range(0, +10)):
                assert monos[i] == (a, b, c)
                i += 1
                tested += 1


    monos.sort(key = totrevlex)
    i = 0
    for tot in reversed(range(0, +30)):
        for c in reversed(range(0, +10)):
            for b in reversed(range(0, +10)):
                a = tot - b - c
                if a >= +10 or a < 0:
                    continue
                assert monos[i] == (a, b, c)
                i += 1
                tested += 1

    monos.sort(key = totlex)
    i = 0
    for tot in reversed(range(0, +30)):
        for a in reversed(range(0, +10)):
            for b in reversed(range(0, +10)):
                c = tot - a - b
                if c >= +10 or c < 0:
                    continue
                assert monos[i] == (a, b, c)
                i += 1
                tested += 1

    print("tested : " + str(tested))

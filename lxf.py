from functools import reduce

def str2num(s):
    try:
        return int(s)
    except ValueError as e:
        print(f"{type(e).__name__} : {e}")
def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    try:
        return reduce(lambda acc, x: acc + x, ns)
    except TypeError as e:
            print(f"{type(e).__name__} : {e}")
def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)

main()

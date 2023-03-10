import math
from time import time


def _fsqrt(n):
    return math.copysign(math.sqrt(math.fabs(n)), n)


def num2sqrts(n, max_num=1000, count_loops=False):
    if n >= 0:
        mid = math.floor((n / 2) ** 2) + 0.5
    elif n < 0:
        mid = math.ceil(-(n / 2) ** 2) - 0.5
    actual_mid = n / 2
    loops = 1
    t = 0.5
    while True:
        a = _fsqrt(mid + t)
        d = math.fabs(a - actual_mid)
        b = actual_mid - d
        b = _fsqrt(math.copysign(round(b ** 2), b))
        if abs(a ** 2) > max_num or abs(b ** 2) > max_num:
            if count_loops:
                return loops
            return
        if math.isclose(a + b, n):
            if count_loops:
                return loops
            return int(round(math.copysign(a ** 2, a))), \
                int(round(math.copysign(b ** 2, b)))
        loops += 1
        t += 1


def perform1():
    # 性能测试1
    from progress.bar import Bar
    import matplotlib.pyplot as plt
    import numpy as np
    mat = np.zeros((201, 201))
    bar = Bar("Processing", max=201 * 201, suffix="%(percent)d%%")
    for x in range(-100, 101):
        for y in range(-100, 101):
            if x == y:
                mat[x + 100][-y + 100] = 1
            else:
                mat[x + 100][-y + 100] = num2sqrts(_fsqrt(x) + _fsqrt(y), count_loops=True)
            bar.next()
    fig, ax = plt.subplots()
    img = ax.matshow(mat)
    fig.colorbar(img, ax=ax)
    ax.set_xlabel("x")
    ax.xaxis.set_major_formatter(lambda x, pos: int(x - 100))
    ax.set_ylabel("y")
    ax.yaxis.set_major_formatter(lambda y, pos: int(-y + 100))
    fig.savefig("perform1.pdf")
    print()


def perform2():
    # 性能测试2
    from progress.bar import Bar
    import statistics as stat
    from json import dump
    L = []
    analyze = []
    bar = Bar("Processing", max=99 * 5, suffix="%(percent)d%%")
    for _ in range(5):
        l = []
        for n in range(1, 100):
            num = (math.sqrt(1000) - math.sqrt(999)) / n
            start = time()
            for i in range(1, 100):
                if num2sqrts(num * i) is not None:
                    bar.next()
                    break
            l.append(time() - start)
        L.append(l)
        slope, intercept = stat.linear_regression(range(1, 100), l)
        correlation = stat.correlation(range(1, 100), l)
        analyze.append({"slope": slope, "intercept": intercept, "correlation": correlation})
    dump({"data": L, "analyze": analyze}, open("perform2.json", "w+"), indent="\t")
    print()


if __name__ == "__main__":
    from sys import argv
    if argv[1] == "p1":
        perform1()
    elif argv[1] == "p2":
        perform2()

from multiprocessing import Process
from threading import Thread
import time


def fibonacci(n):
    if n == 1 or n == 2:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def track_fib_time_default(iters, n):
    times = 0.
    s = time.time()
    for i in range(iters):
        fibonacci(n)
    e = time.time()
    return e - s


def track_fib_time_thread(iters, n):
    thrds = []
    s = time.time()
    for i in range(iters):
        t = Thread(target=fibonacci, args=(n,))
        thrds.append(t)
        t.start()

    for t in thrds:
        t.join()
    e = time.time()

    return e - s


def track_fib_time_process(iters, n):
    prcs = []
    s = time.time()
    for i in range(iters):
        p = Process(target=fibonacci, args=(n,))
        prcs.append(p)
        p.start()

    for p in prcs:
        p.join()
    e = time.time()

    return e - s


def main():
    iters = 10
    n = 35

    with open('artefacts/fib_time.txt', 'w') as f:
        f.write(f'fib({n})*{iters} default: {track_fib_time_default(iters, n):.5f} s.\n')
        f.write(f'fib({n})*{iters} thread: {track_fib_time_thread(iters, n):.5f} s.\n')
        f.write(f'fib({n})*{iters} process: {track_fib_time_process(iters, n):.5f} s.\n')


if __name__ == '__main__':
    main()

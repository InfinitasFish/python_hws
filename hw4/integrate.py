import math
import time
import concurrent.futures
import os


def integrate_segment(f, a, b, n_iter, start, end):
    acc = 0
    step = (b - a) / n_iter
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type):
    if executor_type == 'thread':
        Executor = concurrent.futures.ThreadPoolExecutor
    elif executor_type == 'process':
        Executor = concurrent.futures.ProcessPoolExecutor
    else:
        raise ValueError('invalid executor: integrate()')

    segment_size = n_iter // n_jobs
    segments = []

    for i in range(n_jobs):
        s = i * segment_size
        e = (i + 1) * segment_size if i < (n_jobs - 1) else n_iter
        segments.append((s, e))

    with Executor(max_workers=n_jobs) as executor:
        futures = [
            executor.submit(integrate_segment, f, a, b, n_iter, s, e)
            for s, e in segments
        ]
        seg_sums = [future.result() for future in concurrent.futures.as_completed(futures)]

    return sum(seg_sums)


def main():
    cpu_count = os.cpu_count()
    n_jobs_steps = range(1, cpu_count * 2 + 1)

    for nj in n_jobs_steps:
        s = time.time()
        thread_sum = integrate(math.cos, 0, math.pi / 2, n_jobs=nj, executor_type='thread')
        e = time.time()

        with open('artefacts/integrate.txt', 'a') as f:
            f.write(f'thread integrate() with {nj} jobs took {(e-s):.5f} s.\n')

        s = time.time()
        process_sum = integrate(math.cos, 0, math.pi / 2, n_jobs=nj, executor_type='process')
        e = time.time()
        with open('artefacts/integrate.txt', 'a') as f:
            f.write(f'process integrate() with {nj} jobs took {(e-s):.5f} s.\n')


if __name__ == '__main__':
    main()

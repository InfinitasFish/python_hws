from multiprocessing import Queue, Process
from codecs import encode
import sys
import time


def process_a(inp_queue, out_queue, log_fname):
    while True:
        m = inp_queue.get()
        ml = m.lower()
        out_queue.put(ml)
        with open(log_fname, 'a') as f:
            f.write(f'time: {time.time():.5f}\t process A got "{m}" -> out "{ml}"\n')


def process_b(inp_queue, out_queue, log_fname):
    while True:
        m = inp_queue.get()
        time.sleep(5//2)  # too long
        r13m = encode(m, 'rot13')
        out_queue.put(r13m)
        with open(log_fname, 'a') as f:
            f.write(f'time: {time.time():.5f}\t process B got "{m}" -> out "{r13m}"\n')


def main():
    main_messages = Queue()
    a_b_messages = Queue()
    b_main_cmesages = Queue()

    log_fname = 'AB_log.txt'
    proc_a = Process(target=process_a, args=(main_messages, a_b_messages, log_fname, ))
    proc_b = Process(target=process_b, args=(a_b_messages, b_main_cmesages, log_fname, ))

    proc_a.start()
    proc_b.start()

    while True:
        orig_m = sys.stdin.readline().strip()
        if orig_m == 'exit':
            break
        main_messages.put(orig_m)

    proc_a.terminate()
    proc_b.terminate()


if __name__ == '__main__':
    main()
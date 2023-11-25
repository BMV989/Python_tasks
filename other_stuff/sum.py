import multiprocessing as mp
import os
import time

NUMBER_SIZE = 4


def calc_sum(k, n, s):
    s0 = 0
    with open('data.bin', 'rb') as f:
        size = f.seek(0, 2)
        f.seek(0, 0)
        chunk_size = size // n
        f.seek(k*chunk_size, 0)
        for i in range(chunk_size//NUMBER_SIZE):
            num = int.from_bytes(f.read(NUMBER_SIZE), 'big')
            s0 += num
        s.value += s0


def main():
    process_count = os.cpu_count()
    t0 = time.perf_counter()

    processes = []
    s = mp.Value('l', 0, lock=True)

    for i in range(process_count):
        proc = mp.Process(
            target=calc_sum, args=(i, process_count, s))
        processes.append(proc)
        proc.start()

    for process in processes:
        process.join()

    t1 = time.perf_counter()
    print((t1 - t0), s.value)


if __name__ == "__main__":
    main()

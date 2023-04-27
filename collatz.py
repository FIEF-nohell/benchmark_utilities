from tqdm import tqdm
import cpuinfo
import random
import psutil
import time

# ANSI escape codes for colors
class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

# Get CPU stats
def sys_info(num_threads=None, num_cores=None, cpu_name=None):
    num_threads = psutil.cpu_count(logical=True)
    num_cores = psutil.cpu_count(logical=False)
    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    return [num_threads, num_cores, cpu_name]

class CollatzResponse:
    def __init__(self, n, sequence, length):
        self.number = n
        self.sequence = sequence
        self.length = length

    def __str__(self):
        # Sequence: {self.sequence}\n
        return f"Number: {self.number}\nLength: {self.length}\n"

def collatz_sequence(n):
    number = n
    sequence = [n]

    while n != 1:
        if n % 2 == 0:  # n is even
            n = n // 2
        else:  # n is odd
            n = 3 * n + 1

        sequence.append(n)
    length = len(sequence)
    return CollatzResponse(number, sequence, length)

if __name__ == "__main__":

    benchmark_length = 15

    system_info = sys_info()
    print(f"{Color.CYAN}\n-------------------------------------------\n")
    print(f"{system_info[2]}")
    print(f"Operating with {system_info[1]} Cores and {system_info[0]} Threads\n{Color.GREEN}")
    print(f"Running initial performance test...\n")
    print(f"The test should ensure that the benchmark length of {benchmark_length} seconds is adjusted to each system.")
    print(f"It will not go to 100%, it will stop earlier depending on your system.\n")

    depth = 1000000
    second_started = False

    start_time = time.time()
    start_time2 = time.time()
    num = []
    for x in tqdm(range(1, (depth + 1)), desc="Testing", unit="col"):
        n = random.randint(1, 100000000000000000)
        response = collatz_sequence(n)
        if(time.time() - start_time > 0.5):
            if(second_started == False):
                second_started = True
                start_time2 = time.time()
                num.append(x)
            if(time.time() - start_time2 > 1):
                num.append(x)
                break
    
    approx_speed = (num[1] - num[0])
    print(f"")

    depth = approx_speed * benchmark_length
    start_time = time.time()
    for x in tqdm(range(1, (depth + 1)), desc="Benchmark", unit="col"):
        n = random.randint(1, 100000000000000000)
        response = collatz_sequence(n)
    total_time = time.time() - start_time
    speed = depth / total_time
    
    print(f"\n{Color.RED}Score: {(speed):.2f}")
    print(f"{Color.CYAN}units in collatz sequences/sec | more is better")

    print(f"{Color.CYAN}\n-------------------------------------------{Color.RESET}\n")
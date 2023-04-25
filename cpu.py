from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import cpuinfo
import psutil
import time
import math

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

# Function to perform arithmetic operations linearly
def linear_workload():
    result = 0
    for i in range(5000):
        result += i
        result *= i
    return result

# Function to benchmark single-core performance
def single_core_benchmark(n):
    start_time = time.time()
    for _ in tqdm(range(n), desc="Single-core benchmark", unit="seq"):
        _ = linear_workload()
    end_time = time.time()
    return end_time - start_time

# Function to benchmark multi-core performance
def multi_core_benchmark(n):
    system_info = sys_info()
    num_threads = system_info[0]

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        with tqdm(total=n, desc="Multi-core benchmark", unit="seq") as progress_bar:
            futures = [executor.submit(linear_workload) for _ in range(n)]
            for _ in as_completed(futures):
                progress_bar.update(1)
    end_time = time.time()

    return (end_time - start_time)

if __name__ == "__main__":
    system_info = sys_info()
    bench_depth = 5000
    print(f"{Color.CYAN}\n-------------------------------------------\n")
    print(f"{system_info[2]}")
    print(f"Operating with {system_info[1]} Cores and {system_info[0]} Threads\n{Color.GREEN}")

    # Benchmark single-core performance
    single_core_time = single_core_benchmark(math.ceil(bench_depth/system_info[0]))

    # Benchmark multi-core performance
    multi_core_time = multi_core_benchmark(bench_depth)

    print(f"\n{Color.RED}Single-core Score: {((bench_depth/system_info[0])/single_core_time):.2f}")
    print(f"Multi-core Score: {(bench_depth/multi_core_time):.2f}")
    print("units in sequences/sec | more is better")

    print(f"{Color.CYAN}\n-------------------------------------------{Color.RESET}\n")

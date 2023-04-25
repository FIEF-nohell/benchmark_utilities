import win32com.client
from tqdm import tqdm
import numpy as np
import psutil
import time

# ANSI escape codes for colors
class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

def get_ram_info_windows():
    wmi = win32com.client.GetObject("winmgmts:")
    ram_info = wmi.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
    counter = 0
    for info in ram_info:
        counter = counter + 1
        manufacturer = info.Manufacturer
        speed = info.Speed
        capacity_gb = int(info.Capacity) / (1024 ** 3)
        memory_type = None

        if info.MemoryType == 24:
            memory_type = "DDR3"
        elif info.MemoryType == 0 or info.MemoryType == 20:
            memory_type = "DDR4"

        print(f"DIMM {counter}:")
        print(f"Manufacturer: {manufacturer}")
        print(f"Using {capacity_gb:.0f}GB {memory_type} at {speed}MHz\n")

def memory_bandwidth_benchmark(size_mb=1024, num_iterations=5):
    array_size = size_mb * 1024 * 1024 // 8  # Convert size to number of double-precision elements
    src = np.random.rand(array_size)  # Generate random source array
    dst = np.empty_like(src)  # Create empty destination array

    start_time = time.perf_counter()
    with tqdm(total=num_iterations, unit='GB', unit_scale=True, unit_divisor=1, desc='Bandwidth') as progress_bar:
        for _ in range(num_iterations):
            np.copyto(dst, src)  # Copy source array to destination array
            progress_bar.update(1)
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    total_size_gb = size_mb * num_iterations / 1024  # Convert total size to GB
    bandwidth = total_size_gb / elapsed_time  # Calculate bandwidth in GB/s

    return bandwidth

if __name__ == "__main__":
    size_mb = 1024
    num_iterations = 50
    
    print(f"{Color.CYAN}\n-------------------------------------------\n")
    get_ram_info_windows()
    print(f"{Color.GREEN}")

    bandwidth = memory_bandwidth_benchmark(size_mb, num_iterations)
    print(f"RAM bandwidth: {bandwidth:.2f} GB/s")

    print(f"{Color.CYAN}\n-------------------------------------------{Color.RESET}\n")
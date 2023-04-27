from tqdm import tqdm
import random
import time

# ANSI escape codes for colors
class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

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

best = response = collatz_sequence(1)

start_time = time.time()
for x in tqdm(range(1, 100001), desc="Searching", unit="num"):
    n = random.randint(1, 100000000000000000)
    response = collatz_sequence(n)

    if(response.length > best.length):
        best = response
total_time = time.time() - start_time

print(f"\n\n{total_time:.2f} seconds\n")
print(best)
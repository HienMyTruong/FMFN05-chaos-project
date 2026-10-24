import matplotlib.pyplot as plt
import math
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor


SEED = 0.42
EPSILON = 0.001
MAX_ITERATIONS = 20
REALIZATIONS = 10_000
NOISE_SEED = 12345


def shannon_entropy(p_one):
    p_zero = 1 - p_one

    entropy = 0

    if p_zero > 0:
        entropy -= p_zero * math.log2(p_zero)

    if p_one > 0:
        entropy -= p_one * math.log2(p_one)

    return entropy

def plot_entropy(ones):
    iterations = np.arange(1, MAX_ITERATIONS + 1)

    entropies = []

    for number_of_ones in ones:
        p_one = number_of_ones / REALIZATIONS
        entropies.append(shannon_entropy(p_one))

    theoretical_n = math.log(1 / EPSILON) / math.log(2)

    plt.plot(iterations, entropies, marker="o")

    plt.axvline(
        theoretical_n,
        linestyle="--",
        label=f"Theoretical N = {theoretical_n:.2f}"
    )

    plt.axhline(
        1,
        linestyle=":",
        label="Maximum entropy"
    )

    plt.xlabel("Iteration N")
    plt.ylabel("Shannon entropy H(B_N)")
    plt.title("Shannon entropy over iteration number")

    plt.xticks(iterations)
    plt.ylim(0, 1.05)

    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    chaotic = ChaoticShuffle(SEED, EPSILON)
    extractor = BitExtractor(chaotic)

    np.random.seed(NOISE_SEED)

    ones = np.zeros(MAX_ITERATIONS, dtype=int)

    for _ in range(REALIZATIONS):
        chaotic.x = SEED

        for n in range(MAX_ITERATIONS):
            ones[n] += extractor.next_bit()

    print("N   P(0)       P(1)       H(B_N)")
    print("-----------------------------------")

    for n in range(MAX_ITERATIONS):
        p_one = ones[n] / REALIZATIONS
        p_zero = 1 - p_one
        entropy = shannon_entropy(p_one)

        print(
            f"{n + 1:2d}  "
            f"{p_zero:.6f}   "
            f"{p_one:.6f}   "
            f"{entropy:.6f}"
        )

    theoretical_n = math.log(1 / EPSILON) / math.log(2)

    print()
    print(f"Theoretical N ≈ {theoretical_n:.2f}")

    plot_entropy(ones)


if __name__ == "__main__":
    main()

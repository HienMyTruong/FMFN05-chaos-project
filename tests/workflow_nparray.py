import numpy as np
from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor
from stats_test import BasicStats

# 0.001 < epsilon < 0.01

SEED = 0.42
EPSILON = 0.01
MEGABITS = 1000000


chaotic_floats = ChaoticShuffle(
    seed=SEED,
    ep=EPSILON
)

floats = [
    chaotic_floats.next_chaotic_float()
    for _ in range(MEGABITS)
]

chaotic_bits = ChaoticShuffle(
    seed=SEED,
    ep=EPSILON
)

extractor = BitExtractor(
    chaotic_bits
)

bits = [
    extractor.next_bit()
    for _ in range(MEGABITS)
]


stats = BasicStats(
    floats=floats,
    bits=bits
)

stats.test_all(
    logistic_map=True,
    max_lags=1000
)



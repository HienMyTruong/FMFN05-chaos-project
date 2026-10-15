import numpy as np

from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor


EPSILON = 0.0001
SEED = 0.42
MEGABITS = 1000000


NUMBER_OF_BITS = 50

chaotic = ChaoticShuffle(0.42, 0.00001)
extractor = BitExtractor(chaotic)

bits_ = [extractor.next_bit() for _ in range(NUMBER_OF_BITS)]
bits_ = np.asarray(bits_, dtype=np.uint8)

print(bits_)


import numpy as np
from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor

epsilon = 0.0001
chaotic = ChaoticShuffle(0.42, epsilon)
extractor = BitExtractor(chaotic)


MEGABITS = 1000000


bits = [extractor.next_bit() for _ in range(MEGABITS)]

von_neumann_bits = [
    extractor.next_von_neumann_bit()
    for _ in range(MEGABITS)
]


sequence = np.array(bits, dtype=np.uint8)

print(bits)





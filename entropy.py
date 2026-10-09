from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor
from collections import Counter
import math



class Entropy:
    def __init__(self, bits):
        self.bits = bits

    @staticmethod
    def H(p):
        if p == 0.0:
            return 0.0

        return -p * math.log2(p)


    def shannon_entropy(self):
        number_of_bits = len(self.bits)

        if number_of_bits == 0:
            return 0.0

        ones = sum(self.bits)
        p_ones = ones / number_of_bits
        p_zeros = 1.0 - p_ones

        if p_zeros == 0.0 or p_ones == 0.0:
            return 0.0

        return self.H(p_zeros) + self.H(p_ones)

    def entropy_rate(self, k):
        def block_entropy(k):
            number_of_blocks = len(self.bits) - k + 1

            if number_of_blocks <= 0:
                return 0.0

            counts = Counter(
                tuple(self.bits[i:i + k])
                for i in range(number_of_blocks)
            )

            entropy = 0.0

            for count in counts.values():
                p = count / number_of_blocks
                entropy += self.H(p)

            return entropy

        if k == 1:
            return block_entropy(1)

        return block_entropy(k) - block_entropy(k - 1)


MEGABITS = 1000000

chaotic = ChaoticShuffle(0.42)
extractor = BitExtractor(chaotic)

bits_ = [extractor.next_bit() for _ in range(2*MEGABITS)]

entropy = Entropy(bits_)

print(entropy.entropy_rate(11))
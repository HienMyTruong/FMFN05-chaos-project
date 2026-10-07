from bit_extractor import BitExtractor
import math

class Entropy:
    def __init__(self, bits):
        self.bits = bits

    def shannon_entropy(self):
        number_of_bits = len(self.bits)

        if number_of_bits == 0:
            return 0.0

        ones = sum(self.bits)
        p_ones = ones / number_of_bits
        p_zeros = 1.0 - p_ones

        if p_zeros == 0.0 or p_ones == 0.0:
            return 0.0

        return -(p_zeros * math.log2(p_zeros) + p_ones * math.log2(p_ones))
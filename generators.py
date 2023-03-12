"""
generators
==========

Code for generating waveforms
"""
import math
from consts import SAMPLE_RATE, Waveform


def sine(frequency: int, length: float) -> Waveform:
    """
    Generate a sine wave at the given frequency
    """
    samples = []
    for i in range(int(SAMPLE_RATE * length)):
        samples.append(
            math.sin(
                i / SAMPLE_RATE
                * 2 * math.pi
                * frequency
            ))
    return samples


def saw(frequency: int, length: float) -> Waveform:
    """
    Generate a saw wave at the given frequency
    """
    samples = []
    alternation_rate = 1 / frequency * SAMPLE_RATE
    for i in range(int(SAMPLE_RATE * length)):
        # Negate values so saw edge is rising
        samples.append(-(
            i % alternation_rate  # Base value
            / (alternation_rate / 2)  # Get in range of 0-2
            - 1  # subtract 1
        ))
    return samples


def square(frequency: int, length: float) -> Waveform:
    """
    Generate a square wave at the given frequency
    """
    samples = []
    alternation_rate = 1 / frequency * SAMPLE_RATE
    for i in range(int(SAMPLE_RATE * length)):
        if i % alternation_rate > alternation_rate / 2:
            samples.append(1.0)
        else:
            samples.append(-1.0)
    return samples

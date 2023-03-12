"""
operators
==========

Code for operating on waveforms
"""
import math
from consts import Waveform, SAMPLE_LENGTH


def normalise(wav: Waveform) -> Waveform:
    """
    Normalises a waveform, returning a waveform where the maximum amplitude is
    1.0.
    """
    # Scale to use is the lowest negative value or the highest positive value,
    # whichever is bigger
    factor = 1 / max(max(wav), -min(wav))

    # Return the waveform scaled by the required amount
    return scale(wav, factor)


def add(wav1: Waveform, wav2: Waveform) -> Waveform:
    """
    Add two waveforms together and return the result
    """
    result = []
    for v1, v2 in zip(wav1, wav2):
        result.append(v1 + v2)
    return result


def subtract(wav1: Waveform, wav2: Waveform) -> Waveform:
    """
    Subtract wav2 from wav1 and return the result
    """
    result = []
    for v1, v2 in zip(wav1, wav2):
        result.append(v1 - v2)
    return result


def scale(wav: Waveform, factor: float) -> Waveform:
    """
    Multiply the given waveform by factor, then return the result
    """
    # Use a list comprehension to scale the values
    return [v * factor for v in wav]


def stretch(wav: Waveform, factor: float) -> Waveform:
    """
    Stretch the given waveform by factor, then return the result
    """
    result = []
    for i in range(SAMPLE_LENGTH):
        # Calculate sample position in original sample
        og_index = i / factor

        # Prevent ourselves from going past the end of the sample by pretending
        # the samples loop infinitely
        og_index %= SAMPLE_LENGTH

        # Grab the two samples around the required point
        start_val = wav[math.floor(og_index)]
        end_val = wav[math.ceil(og_index)]

        # And interpolate between them
        # Technically you could do better by doing some wild quadratic stuff,
        # but we'll just do a linear interpolation for the sake of my sanity
        sub_position = og_index - math.floor(og_index)
        # It's just a weighted average
        result.append(
            (start_val * sub_position)
            + (end_val * (1 - sub_position))
        )

    return result

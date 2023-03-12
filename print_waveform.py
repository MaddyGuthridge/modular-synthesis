"""
Print waveform
==============

Code for printing waveforms to the user's terminal.
"""
from os import get_terminal_size
from colorama import Fore

from consts import WAVE_HEIGHT, WAVE_CHAR, SPACE_CHAR


def print_waveform(wav: list[float]):
    """
    Prints the given waveform to the output.

    Waveforms are printed as one character per sample. The samples are trimmed
    to avoid cluttering the terminal.

    Any clipping values (outside the range -1..1) are printed as red
    """
    # Distribution of amplitudes to facilitate drawing the waveforms
    # This categorises each sample point into WAVE_HEIGHT groups, so that we
    # can cleanly print it out line by line.
    # Each value is a set of indexes, which are the sample indexes that belong
    # in that group of the distribution
    wave_distribution: list[set[int]] = [set() for _ in range(WAVE_HEIGHT + 1)]
    # Keep track of values that are clipping (amplitude > 1)
    clip_upper = set()
    clip_lower = set()
    for i, value in enumerate(wav):
        # Handle clipping values
        if value > 1:
            clip_upper.add(i)
        elif value < -1:
            clip_lower.add(i)
        else:
            # Value lies within the main waveform, find out where to put it in
            # our wave distribution
            rounded_value = round((value + 1) / 2 * WAVE_HEIGHT)
            wave_distribution[rounded_value].add(i)

    line_length = get_terminal_size().columns

    # Print the upper clipping values
    print(Fore.RED, end='')
    for i in range(line_length):
        # If the index is in our set of clipping indexes, print it
        if i in clip_upper:
            print(WAVE_CHAR, end='')
        # Otherwise, print empty space
        else:
            print(SPACE_CHAR, end='')
    print(Fore.RESET, end='\n')

    # Now print all the main values
    # We need to loop over them backwards, or it'll be upside-down
    for line in reversed(wave_distribution):
        for i in range(line_length):
            # If the index is in our set of indexes for this line, print it
            if i in line:
                print(WAVE_CHAR, end='')
            # Otherwise, print empty space
            else:
                print(SPACE_CHAR, end='')

    # Finally, print the lower clipping values
    print(Fore.RED, end='')
    for i in range(line_length):
        # If the index is in our set of clipping indexes, print it
        if i in clip_lower:
            print(WAVE_CHAR, end='')
        # Otherwise, print empty space
        else:
            print(SPACE_CHAR, end='')
    print(Fore.RESET, end='\n')

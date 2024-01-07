"""
Modular Synthesis
=================

A simple program for generating and manipulating waveforms.

This project isn't intended to be performant. It's just a little demo I made
for fun.

Made with <3 by Miguel Guthridge
"""
import sys
import wave
import struct
import generators as gen
import operators as op
from print_waveform import print_waveform
from consts import Waveform, SAMPLE_RATE


WaveformsLibrary = dict[str, Waveform]


class InvalidInput(ValueError):
    pass


def print_help():
    print("\n".join([
        "Available commands:",
        " - gen [kind] [freq] [length] [name] - generate a waveform",
        " - op add [wav1] [wav2] [name] - add [wav1] and [wav2] values",
        " - op sub [wav1] [wav2] [name] - subtract [wav1] values from [wav2]",
        " - op norm [wav] [name] - normalise [wav]",
        " - op scale [wav] [amount] [name] - scale [wav] by [amount]",
        " - op stretch [wav] [amount] [name] - stretch [wav] by [amount]",
        " - op append [wav1] [wav2] [name] - append [wav1] to [wav2]",
        " - print [wav] - print the waveform [wav]",
        " - save [wav] [file] - save the waveform [wav] to [file]",
        " - list - list loaded waveforms",
        " - help - display this message",
        " - quit",
        "",
        "Where:",
        " - [kind] - kind of waveform to generate (sine, saw, square)",
        " - [freq] - frequency in Hz",
        " - [length] - length of sample",
        " - [name] - name to associate with waveform",
        "",
    ]))


def handle_generators(kind: str, freq: int, length: float) -> Waveform:
    match kind:
        case "sine" | "sin":
            generator = gen.sine
        case "saw":
            generator = gen.saw
        case "square":
            generator = gen.square
        case "triangle":
            generator = gen.tri
        case _:
            raise InvalidInput("Unknown generator kind")
    return generator(freq, length)


def handle_operators(
    kind: str,
    args: list[str],
    wavs: WaveformsLibrary,
) -> Waveform:
    match kind:
        case "add" | "+":
            wav1 = wavs[args[0]]
            wav2 = wavs[args[1]]
            return op.add(wav1, wav2)
        case "sub" | "-":
            wav1 = wavs[args[0]]
            wav2 = wavs[args[1]]
            return op.subtract(wav1, wav2)
        case "norm" | "=":
            wav = wavs[args[0]]
            return op.normalise(wav)
        case "scale" | "*":
            wav = wavs[args[0]]
            factor = float(args[1])
            return op.scale(wav, factor)
        case "stretch":
            wav = wavs[args[0]]
            factor = float(args[1])
            return op.stretch(wav, factor)
        case "append":
            wav1 = wavs[args[0]]
            wav2 = wavs[args[1]]
            return op.append(wav1, wav2)
        case _:
            raise InvalidInput("Unknown operator kind")


def save_wave(wav: Waveform, filename: str):
    """
    Save a waveform to the given filename
    """
    # https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
    with wave.open(filename, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        for v in wav:
            value = round(v * 32767)
            data = struct.pack('<h', value)
            f.writeframesraw(data)


def main() -> None:
    """
    Main loop of the program
    """
    # Don't print if not interactive
    if sys.stdin.isatty():
        print("Modular Synthesis")
        print()
        print_help()

    wavs: dict[str, list[float]] = {}

    while True:
        if sys.stdin.isatty():
            prompt = "Enter a command: "
        else:
            prompt = ""
        cmd, *args = input(prompt).split()

        # Dodgy error handling
        try:
            match cmd:
                case "g" | "gen":
                    kind = args[0]
                    freq = int(args[1])
                    length = float(args[2])
                    name = args[3]
                    wavs[name] = handle_generators(kind, freq, length)
                case "o" | "op":
                    kind, *args, name = args
                    wavs[name] = handle_operators(kind, args, wavs)
                case "p" | "print":
                    name = args[0]
                    print_waveform(wavs[name])
                case "s" | "save":
                    name = args[0]
                    file = args[1]
                    save_wave(wavs[name], file)
                case "l" | "list":
                    if len(wavs) == 0:
                        print("No waveforms generated")
                    else:
                        for name in wavs.keys():
                            print(f" - {name}")
                case "h" | "help":
                    print_help()
                case "q" | "quit" | "exit":
                    print("Goodbye!")
                    return
                case _:
                    print(f"Unknown command: {cmd}")
        except InvalidInput as e:
            print(f"Invalid input: {e.args[0]}")
        except IndexError:
            print(f"Invalid arguments for command: {cmd}")
        except KeyError:
            print("Invalid waveform name")


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        if sys.stdin.isatty():
            print("quit\nGoodbye!")

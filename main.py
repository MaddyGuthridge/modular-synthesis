"""
Modular Synthesis
=================

A simple program for generating and manipulating waveforms. Used to demonstrate
modules for COMP1010 at UNSW.

Waveform generation:
    The waveform generation functions generate lists of sample points, where a
    sample is taken every 10000th of a second. Only 1/10th of a second (1000
    samples) is generated for the sake of performance.

Waveform printing:
    The waveforms are printed as one character per sample. The samples are cut
    short so as not to clutter the terminal.

Made with <3 by Miguel Guthridge
"""
import generators as gen
import operators as op
from print_waveform import print_waveform
from consts import Waveform


WaveformsLibrary = dict[str, Waveform]


class InvalidInput(ValueError):
    pass


def print_help():
    print("\n".join([
        "Available commands:",
        " gen [kind] [freq] [name] - generate a waveform",
        " op add [wav1] [wav2] [name] - add [wav1] and [wav2] together",
        " op sub [wav1] [wav2] [name] - subtract [wav1] from [wav2]",
        " op norm [wav] [name] - normalise [wav]",
        " op scale [wav] [amount] [name] - scale [wav] by [amount]",
        " op stretch [wav] [amount] [name] - stretch [wav] by [amount]",
        " p [wav] - print the waveform [wav]",
        " l - list stored waveforms",
        " q - quit",
        "",
        "Where:",
        " [kind] - kind of waveform to generate (sine, saw, square)",
        " [freq] - frequency in Hz",
        " [name] - name to associate with waveform",
        "",
    ]))


def handle_generators(kind: str, freq: int) -> Waveform:
    match kind:
        case "sine" | "sin":
            generator = gen.sine
        case "saw":
            generator = gen.saw
        case "square":
            generator = gen.square
        case _:
            raise InvalidInput("Unknown generator kind")
    return generator(freq)


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
        case _:
            raise InvalidInput("Unknown operator kind")


def main() -> None:
    """
    Main loop of the program
    """
    print("Modular Synthesis")
    print()
    print_help()

    wavs: dict[str, list[float]] = {}

    while True:
        cmd, *args = input("Enter a command: ").split()

        # Dodgy error handling
        try:
            match cmd:
                case "gen":
                    kind = args[0]
                    freq = int(args[1])
                    name = args[2]
                    wavs[name] = handle_generators(kind, freq)
                case "op":
                    kind, *args, name = args
                    wavs[name] = handle_operators(kind, args, wavs)
                case "p":
                    name = args[0]
                    print_waveform(wavs[name])
                case "l":
                    if len(wavs) == 0:
                        print("No waveforms generated")
                    else:
                        for name in wavs.keys():
                            print(f" - {name}")
                case "q":
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
        print("Goodbye!")

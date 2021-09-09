#!/usr/bin/env python3

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
from doc import ascii_art, parse_arguments
assert numpy  # avoid "imported but unused" message (W0611)
from pedalboard import (
    Pedalboard,
    Chorus,
    Compressor,
    Convolution,
    Distortion,
    Gain,
    HighpassFilter,
    LadderFilter,
    Limiter,
    LowpassFilter,
    NoiseGate,
    Phaser,
    Reverb
)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def make_board(effects, options):
    board = Pedalboard([], sample_rate=int(options["--samplerate"]))
    for effect_data in effects:
        effect_name = list(effect_data.keys())[0]
        class_name = ''.join(p.capitalize() for p in effect_name.split('_'))
        effect = globals()[class_name](**effect_data[effect_name])
        board.append(effect)
    return board


def play(options, board):
    def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        indata = board(indata)
        outdata[:] = indata

    try:
        with sd.Stream(device=(options["--input-device"], options["--output-device"]),
                       samplerate=options["--samplerate"], blocksize=options["--blocksize"],
                       dtype=options["--dtype"], latency=options["--latency"],
                       channels=options["--channels"], callback=callback):
            print(ascii_art)
            print('press return to quit')
            input()
    except KeyboardInterrupt:
        exit('')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))


def main():
    options, effects = parse_arguments()
    board = make_board(effects, options)
    play(options, board)


if __name__ == '__main__':
    main()

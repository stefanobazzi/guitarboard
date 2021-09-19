#!/usr/bin/env python3
import numpy as np
import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
from .doc import ascii_art
from .parser import parse_arguments

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


def make_board(effects, options):
    board = Pedalboard([], sample_rate=options.samplerate)
    for effect_data in effects:
        class_name = effect_data['namespace'].effect
        if class_name:
            Class = globals().get(class_name.capitalize())
            try:
                effect = Class(**effect_data['kwargs'])
                board.append(effect)
            except ValueError as err:
                print(f"Error: {err}")
                exit(0)
    # print(board)
    return board


def play(options, board):
    def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        indata = board(indata)

        outdata[:] = indata

    try:
        with sd.Stream(device=(options.input_device, options.output_device),
                       samplerate=options.samplerate,
                       blocksize=options.blocksize,
                       dtype=options.dtype, latency=options.latency,
                       channels=options.channels, callback=callback):

            print(ascii_art)
            print('press return to quit')
            input()
    except KeyboardInterrupt:
        exit('')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))


def main():
    options, effects = parse_arguments()
    # print(options)
    board = make_board(effects, options)
    play(options, board)


if __name__ == '__main__':
    main()

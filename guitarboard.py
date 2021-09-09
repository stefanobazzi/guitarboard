#!/usr/bin/env python3

import argparse

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


def _parse_arguments():
    parser = argparse.ArgumentParser(prog='Guitar Board', add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-i', '--input-device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-o', '--output-device', type=int_or_str,
        help='output device (numeric ID or substring)')
    parser.add_argument(
        '-c', '--channels', type=int, default=2,
        help='number of channels')
    parser.add_argument('--dtype', help='audio data type')
    parser.add_argument('--samplerate', type=float, help='sampling rate',
                        default=44100)
    parser.add_argument('--blocksize', type=int, help='block size')
    parser.add_argument('--latency', type=float, help='latency in seconds')

    # effects
    subparsers = parser.add_subparsers(title="Commands", help="Select a command help")
    effects_parser = subparsers.add_parser('effects', help="Create a chain of effects")
    effects_parser.add_argument('--compressor', nargs=2, type=float)
    effects_parser.add_argument('--distortion', type=float)
    effects_parser.add_argument('--chorus')
    effects_parser.add_argument('--convolution')
    effects_parser.add_argument('--gain')
    effects_parser.add_argument('--highpass-filter')
    effects_parser.add_argument('--ladder-filter')
    effects_parser.add_argument('--limiter')
    effects_parser.add_argument('--lowpass-filter')
    effects_parser.add_argument('--noise-gate')
    effects_parser.add_argument('--phaser')
    effects_parser.add_argument('--reverb')

    args = parser.parse_args(remaining)
    effects_args, unknonwn = effects_parser.parse_known_args()
    print(args)
    print(effects_args, unknonwn)
    return parser, args, effects_args


def _make_board(args, effects_args):
    effects = {}
    board = Pedalboard([], sample_rate=args.samplerate)

    if effects_args.compressor:
        compressor = Compressor(threshold_db=-args.compressor[0],
                                ratio=args.compressor[1])
        effects['compressor'] = compressor
    if effects_args.distortion:
        distortion = Distortion(args.distortion)
        effects['distortion'] = distortion
    if effects_args.chorus:
        chorus = Chorus()
        effects['chorus'] = chorus
    if effects_args.convolution:
        convolution = Convolution()
        effects['convolution'] = convolution
    if effects_args.gain:
        gain = Gain()
        effects['gain'] = gain
    if effects_args.highpass_filter:
        highpass_filter = HighpassFilter()
        effects['highpass_filter'] = highpass_filter
    if effects_args.ladder_filter:
        ladder_filter = LadderFilter()
        effects['ladder_filter'] = ladder_filter
    if effects_args.limiter:
        limiter = Limiter()
        effects['limiter'] = limiter
    if effects_args.lowpass_filter:
        lowpass_filter = LowpassFilter()
        effects['lowpass_filter'] = lowpass_filter
    if effects_args.noise_gate:
        noise_gate = NoiseGate()
        effects['noise_gate'] = noise_gate
    if effects_args.phaser:
        phaser = Phaser()
        effects['phaser'] = phaser
    if effects_args.reverb:
        reverb = Reverb()
        effects['reverb'] = reverb

    # for effect in effects_args:
    #     board.append(effect)
    return board


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
    # print(options, effects)
    board = make_board(effects, options)
    play(options, board)


if __name__ == '__main__':
    main()

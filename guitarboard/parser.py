import argparse
import tempfile
import sounddevice as sd

from pedalboard import (
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


def parse_arguments():
    effects = [
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
    ]
    description = "Play live guitar (or mic) in you shell with python."
    parser = argparse.ArgumentParser(description=description)

    # sounddevice options
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    parser.add_argument('-i', '--input-device', type=int,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-o', '--output-device', type=int,
                        help='output device (numeric ID or substring)')
    parser.add_argument('-c', '--channels', type=int, default=2,
                        help='number of channels')
    parser.add_argument('--dtype', help='audio data type')
    parser.add_argument('--samplerate', type=float, help='sampling rate',
                        default=44100)
    parser.add_argument('--blocksize', type=int, help='block size')
    parser.add_argument('--latency', type=float, help='latency in seconds')
    subparsers = parser.add_subparsers(help="Effects help", dest='effect')

    subparsers_dict = {}
    tmp = tempfile.NamedTemporaryFile()
    effects_dict = {}
    for Effect in effects:
        name = Effect.__name__.lower()
        effects_dict[name] = Effect
        subparser = subparsers.add_parser(name=name, description=Effect.__doc__)
        subparser_args = {}
        default_args = {}
        mandatory_args = {}
        for k, v in Effect.__dict__.items():
            if not k.startswith('_'):
                try:
                    effect = Effect(**subparser_args, **{k: tmp.name for k in
                                                         mandatory_args.keys()})
                    default_args[k] = getattr(effect, k)
                except TypeError:
                    mandatory_args[k] = None
                except RuntimeError:
                    default_args[k] = getattr(effect, k)
                except Exception as e:
                    raise
        subparser_args = {**default_args, **mandatory_args}
        for arg, default in subparser_args.items():
            prefix = '--'
            if default is None:
                prefix = ''
            subparser.add_argument(f"{prefix}{arg}", default=default,
                                   type=type(default))
            subparsers_dict[name] = subparser_args

    selected_effect = []
    main_namespace, other = parser.parse_known_args()
    kwargs = {k: getattr(main_namespace, k) for k in
              subparsers_dict.get(main_namespace.effect, {})}
    selected_effect.append({"namespace": main_namespace, "kwargs": kwargs})
    while other:
        namespace, other = parser.parse_known_args(other)
        kwargs = {k: getattr(namespace, k) for k in
                  subparsers_dict.get(namespace.effect, {})}
        selected_effect.append({"namespace": namespace, "kwargs": kwargs})
    # print(selected_effect)

    if main_namespace.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    return main_namespace, selected_effect

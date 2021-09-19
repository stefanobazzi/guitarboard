from docopt import docopt
import sounddevice as sd


ascii_art = \
""" 
 _____       _ _            ______                     _ 
|  __ \     (_| |           | ___ \                   | |
| |  \/_   _ _| |_ __ _ _ __| |_/ / ___   __ _ _ __ __| |
| | __| | | | | __/ _` | '__| ___ \/ _ \ / _` | '__/ _` |
| |_\ | |_| | | || (_| | |  | |_/ | (_) | (_| | | | (_| |
 \____/\__,_|_|\__\__,_|_|  \____/ \___/ \__,_|_|  \__,_|
"""

name = "guitarboard"

commands = [
    "compressor",
    "distortion",
    "chorus",
    "convolution",
    "gain",
    "highpass-filter",
    "ladder-filter",
    "limiter",
    "lowpass-filter",
    "noise-gate",
    "phaser",
    "reverb",
]
# commands_fmt = ' '.join(f"[{c}]" for c in commands)
commands_fmt = "\n    ".join(commands)
# commands_fmt = "\n    ".join(f"{' ':>33} [{c}] [<args> <b>]" for c in commands)

basic_usage = \
f"""{name}.

Usage:
    guitarboard [options] effects [[command <args>...]...] 
    guitarboard -l

Commands:
    {commands_fmt}

See 'guitarboard help <command>' for more information on a specific command.

Options:
    -h, --help            show this help message and exit
    -l, --list-devices    show list of audio devices and exit
    -i DEVICE, --input-device DEVICE 
                        input device (numeric ID or substring)
    -o DEVICE, --output-device DEVICE
                        output device (numeric ID or substring)
    -c CHANNELS, --channels CHANNELS
                        number of channels [default: 2]
    --dtype DTYPE         audio data type
    --samplerate SAMPLERATE
                        sampling rate [default: 44100]
    --blocksize BLOCKSIZE
                        block size
    --latency LATENCY     latency in seconds
"""

compressor_usage = \
f"""
Usage: 
    effects compressor [threshold_db] [ratio] [attack_ms] [release_ms] 
"""
distortion_usage = \
f"""
Usage:
    effects distortion [options] [<drive_db>] 

Options:
    -h, --help            show this help message and exit
"""
chorus_usage = \
f"""
Usage: 
    effects chorus [rate_hz] [depth] [centre_delay_ms] [feedback] [mix]  
"""
convolution_usage = \
f"""
Usage: 
    effects convolution impulse_response_filename [mix] 
"""
gain_usage = \
f"""
Usage: 
    effects gain [gain_db] 
"""
highpass_filter_usage = \
f"""
Usage: 
    effects highpass-filter [cutoff_frequency_hz] 
"""
ladder_filter_usage = \
f"""
Usage: 
    effects ladder-filter mode 
"""
limiter_usage = \
f"""
Usage: 
    effects limiter [threshold_db] [release_ms] 
"""
lowpass_filter_usage = \
f"""
Usage: 
    effects lowpass-filter [threshold_db] [ratio] [attack_ms] [release_ms]    
"""
noise_gate_usage = \
f"""
Usage: 
    effects noise-gate [threshold_db] [ratio] [attack_ms] [release_ms]   
"""
phaser_usage = \
f"""
Usage: 
    effects phaser [rate_hz] [depth] [centre_frequency_hz] [feedback] [mix] 
"""
reverb_usage = \
f"""
Usage: 
    effects reverb [<room_size>] [<damping>] [<wet_level>] [<dry_level>] [<width>] [<freeze_mode>]

Options:
-h, --help            show this help message and exit
"""

effects_usage = {
    "compressor_usage": compressor_usage,
    "distortion_usage": distortion_usage,
    "chorus_usage": chorus_usage,
    "convolution_usage": convolution_usage,
    "gain_usage": gain_usage,
    "highpass_filter_usage": highpass_filter_usage,
    "ladder_filter_usage": ladder_filter_usage,
    "limiter_usage": limiter_usage,
    "lowpass_filter_usage": lowpass_filter_usage,
    "noise_gate_usage": noise_gate_usage,
    "phaser_usage": phaser_usage,
    "reverb_usage": reverb_usage
}


def cast_value(value):
    if type(value) == str and value.isnumeric():
        return float(value) if '.' in value else int(value)
    return value 


def parse_arguments():
    options = docopt(basic_usage)
    options = {k: cast_value(v) for k, v in options.items()}
    subcommands = []
    if options["--list-devices"]:
        print(sd.query_devices())
        exit(0)
    while options['<args>']:
        arg = options['<args>'].pop(0)
        if arg in commands:
            subcommands.append([arg])
        else:
            if not subcommands:
                subcommands.append([])
            subcommands[len(subcommands) - 1].append(arg)
    effects = []
    for cmd in subcommands:
        cmd_name = cmd[0]
        if cmd_name in commands:
            cmd_name_py = cmd_name.replace('-', '_')
            usage = effects_usage[f"{cmd_name_py}_usage"]
            parsed_cmd = docopt(usage, cmd)
            parsed_cmd.pop(cmd_name)
            parsed_cmd = {k.strip('<').strip('>'): cast_value(v) for k, v in parsed_cmd.items() if v}
            effects.append({cmd_name_py: parsed_cmd})
        else:
            exit(f"{cmd_name} is not a valid command. See '{name} --help'.")
    return options, effects

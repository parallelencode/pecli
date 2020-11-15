#!/bin/env python
import argparse
from pathlib import Path
from parallelencode import Args


def arg_parsing():
    """Command line parsing"""
    parser = argparse.ArgumentParser()

    # cli settings
    cli_group = parser.add_argument_group("pecli 0.1.3 specific options")
    cli_group.add_argument('--logging', type=str, default=None, help='Log file path. Leave unset to log to temp folder')
    cli_group.add_argument('--config', type=Path, help='Parameters file. To be saved/loaded: ' +
                                                       'Video, Audio, Encoder, FFmpeg parameteres')
    cli_group.add_argument('--vmaf_plots', help='Make plots of probes in temp folder', action='store_true')
    #cli_group.add_argument('--help', '-h', action='store_true', help='Print the help menu and the version of the program.')

    # Input/Output/Temp
    io_group = parser.add_argument_group('Input and Output')
    io_group.add_argument('--input', '-i', type=Path, help='Input File')
    io_group.add_argument('--temp', type=Path, default=Path('.temp'), help='Set temp folder path')
    io_group.add_argument('--output_file', '-o', type=Path, default=None, help='Specify output file')
    io_group.add_argument('--mkvmerge', help='Use mkvmerge instead of ffmpeg to concatenate', action='store_true')
    io_group.add_argument('--resume', '-r', help='Resuming previous session', action='store_true')
    io_group.add_argument('--keep', help='Keep temporally folder after encode', action='store_true')

    # Splitting
    split_group = parser.add_argument_group('Splitting')
    split_group.add_argument('--chunk_method', '-cm', type=str, default='vs_lsmash', help='Method for creating chunks',
                             choices=['vs_lsmash', 'segment'])
    split_group.add_argument('--split_method', type=str, default='ffmpeg', help='Specify splitting method',
                             choices=['ffmpeg', 'pyscene', 'time', 'file', 'none'])
    split_group.add_argument('--time_split_interval', '-ts', type=int, default=240,
                             help='Number of frames after which make split if using time splitting')
    # PySceneDetect split
    split_group.add_argument('--threshold', '-tr', type=float, default=0.3, help='ffmpeg/pyscenedetect threshold')

    # AOM Keyframe split
    split_group.add_argument('--reuse_first_pass', help='Reuse the first pass from aom_keyframes split on the chunks',
                             action='store_true')

    # Encoding
    encode_group = parser.add_argument_group('Encoding')
    encode_group.add_argument('--passes', '-p', type=int, default=None, help='Encoding passes', choices=[1, 2])
    encode_group.add_argument('--video_params', '-v', type=str, default=None, help='Encoder specific settings')
    encode_group.add_argument('--encoder', '-enc', type=str, default='aom', help='Choosing encoder',
                              choices=['aom', 'rav1e', 'vpx', 'x265', 'x264'])
    encode_group.add_argument('--workers', '-w', type=int, default=0, help='Number of workers')
    encode_group.add_argument('--no_check', '-n', help='Do not check encodings. NOT recommended', action='store_true')

    # FFmpeg params
    ffmpeg_group = parser.add_argument_group('FFmpeg')
    ffmpeg_group.add_argument('--ffmpeg', '-ff', type=str, default='', help='FFmpeg commands')
    ffmpeg_group.add_argument('--audio_params', '-a', type=str, default='-c:a copy', help='FFmpeg audio settings')
    ffmpeg_group.add_argument('--pix_format', '-fmt', type=str, default='yuv420p', help='FFmpeg pixel format')

    # Vmaf
    vmaf_group = parser.add_argument_group('VMAF')
    vmaf_group.add_argument('--vmaf', help='Calculate and plot vmaf after encode', action='store_true')
    vmaf_group.add_argument('--vmaf_path', type=Path, default=None, help='Path to vmaf models')
    vmaf_group.add_argument('--vmaf_res', type=str, default="1920x1080", help='Resolution used in vmaf calculation')
    vmaf_group.add_argument('--n_threads', type=int, default=None, help='Threads for vmaf calculation')

    # Target Vmaf
    tvmaf_group = parser.add_argument_group('Target VMAF')
    tvmaf_group.add_argument('--vmaf_target', type=float, help='Value of Vmaf to target')
    tvmaf_group.add_argument('--vmaf_steps', type=int, default=4, help='Steps between min and max qp for target vmaf')
    tvmaf_group.add_argument('--min_q', type=int, default=None, help='Min q for target vmaf')
    tvmaf_group.add_argument('--max_q', type=int, default=None, help='Max q for target vmaf')
    tvmaf_group.add_argument('--vmaf_rate', type=int, default=4, help='Framerate for probes, 0 - original')
    tvmaf_group.add_argument('--vmaf_filter', type=str, default=None, help='Filter applied to source at vmaf calcualation. Needed if you crop source')

    va = vars(parser.parse_args())
    if va['input'] is None:
        parser.print_help()
        exit(0)
        return None

    return va


def convert_args(args):
    args.pop("logging")
    args.pop("config")
    args.pop("vmaf_plots")
    return Args(args)

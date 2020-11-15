import atexit
import shlex
import sys
import os

from cli.handle_callbacks import terminate
from pathlib import Path
from parallelencode.encoders import ENCODERS
from distutils.spawn import find_executable
from parallelencode import Args


def set_vmaf(args):
    """
    cli setup for VMAF

    :param args: the Args
    """
    if args['vmaf_path']:
        if not Path(args['vmaf_path']).exists():
            print(f'No such model: {Path(args.vmaf_path).as_posix()}')
            terminate(1)

    if args['vmaf_steps'] < 4:
        print('Target vmaf require more than 3 probes/steps')
        terminate(1)

    encoder = ENCODERS[args['encoder']]

    if args['min_q'] is None:
        args['min_q'], _ = encoder.default_q_range
    if args['max_q'] is None:
        _, args['max_q'] = encoder.default_q_range


def check_exes(args: dict):
    """
    Checking required executables

    :param args: the Args
    """

    if not find_executable('ffmpeg'):
        print('No ffmpeg')
        terminate(1)

    if args['chunk_method'] in ['vs_lsmash']:
        if not find_executable('vspipe'):
            print('vspipe executable not found')
            terminate(1)

        try:
            import vapoursynth
            plugins = vapoursynth.get_core().get_plugins()
        except ModuleNotFoundError:
            print('Vapoursynth is not installed')
            terminate(1)

        if args['chunk_method'] == 'vs_lsmash' and "systems.innocent.lsmas" not in plugins:
            print('lsmash is not installed')
            terminate(1)


def setup_encoder(args: dict):
    """
    Settup encoder params and passes

    :param args: the Args
    """
    encoder = ENCODERS[args['encoder']]

    # validate encoder settings
    settings_valid, error_msg = encoder.is_valid(args)
    if not settings_valid:
        print(error_msg)
        terminate(1)

    if args['passes'] is None:
        args['passes'] = encoder.default_passes

    args['video_params'] = encoder.default_args if args['video_params'] is None \
        else shlex.split(args['video_params'])


def startup_check(args: dict):
    """
    Performing essential checks at startup_check
    Set constant values
    """
    if sys.version_info < (3, 6):
        print('Python 3.6+ required')
        sys.exit()
    if sys.platform == 'linux':
        def restore_term():
            os.system("stty sane")

        atexit.register(restore_term)

    check_exes(args)

    set_vmaf(args)

    setup_encoder(args)

    args['audio_params'] = shlex.split(args['audio_params'])
    args['ffmpeg'] = shlex.split(args['ffmpeg'])

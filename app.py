#!/usr/bin/env python

import os
import re
import shutil

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from chris_plugin import chris_plugin, PathMapper

__version__ = '0.1.4'

DISPLAY_TITLE = r"""
sanitize filenames
"""


parser = ArgumentParser(description='sanitize filenames.'
                                    'retaining only `[./0-9A-Za-z_-]`.'
                                    'The others are changed to be `_`.',
                        formatter_class=ArgumentDefaultsHelpFormatter)


# The main function of this *ChRIS* plugin is denoted by this ``@chris_plugin`` "decorator."
# Some metadata about the plugin is specified here. There is more metadata specified in setup.py.
#
# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='sanitize filenames',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """

    input_dir_str = str(inputdir)
    output_dir_str = str(outputdir)

    print(f'to sanitize: input_dir: {input_dir_str} output_dir: {output_dir_str}')

    for root, the_dirs, the_filenames in os.walk(input_dir_str):
        the_filename_list = list(the_filenames)
        for each_filename in the_filename_list:
            full_filename = os.sep.join([root, each_filename])
            full_out_filename = output_dir_str + full_filename[len(input_dir_str):]
            sanitized_full_out_filename = re.sub(r'[^./0-9A-Za-z_-]+', '_', full_out_filename)
            sanitized_full_out_filename = re.sub(r'_+', '_', sanitized_full_out_filename)

            print(f'to copy: in: {full_filename} out: {sanitized_full_out_filename}')
            sanitized_full_dirname = os.path.dirname(sanitized_full_out_filename)
            os.makedirs(sanitized_full_dirname, exist_ok=True)
            shutil.copyfile(full_filename, sanitized_full_out_filename)


if __name__ == '__main__':
    main()

"""
Configurability script

Methods used for internal configuration of this script.

 -==========================================================================-
    Written for python 2.7 because it is included with Ubuntu 16.04 and I
      wanted to avoid requiring that python 3 also be installed.
 -==========================================================================-
"""

import os
import os.path
import logging

from . import custom_files

logger = logging.getLogger(__name__)


def locate_configuration_directory():
    directory = os.environ.get('CONFIGURABILITY_DIR', None)

    if directory is None:
        logger.warning('Configurability directory not configured')
        exit(0)

    directory = os.path.realpath(directory)
    if not os.path.exists(directory):
        logger.warning('Directory does not exist: %s' % directory)
        exit(0)
    if not os.path.isdir(directory):
        logger.warning('Path is not a directory: %s' % directory)
        exit(0)

    logger.info('Using directory %s' % directory)
    return directory


def read_internal_configuration():
    try:
        configurations = []
        directory = os.environ.get(
            'CONFIGURABILITY_INTERNAL',  # This is available only for debugging purposes
            '/etc/configurability/'
        )
        for file_path in os.listdir(directory):
            configurations.append(
                custom_files.read_custom_file(
                    os.path.join(directory, file_path)
                )[0]
            )

        result = {}
        for configuration in configurations:
            result.update(configuration)
        return result

    except Exception as config_exception:
        logger.critical(
            'Unable to read internal configuration',
            exc_info=config_exception
        )
        exit(1)

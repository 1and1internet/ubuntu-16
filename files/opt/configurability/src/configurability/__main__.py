#!/usr/bin/env python
"""
Configurability script

Main entry point for CLI. See __init__.py for documentation.

 -==========================================================================-
    Written for python 2.7 because it is included with Ubuntu 16.04 and I
      wanted to avoid requiring that python 3 also be installed.
 -==========================================================================-
"""

import logging
import importlib

from . import internal_configuration

logger = logging.getLogger(__name__)


def setup_logging():
    # noinspection SpellCheckingInspection
    logging.basicConfig(
        format='%(asctime)s %(levelname)7s - %(message)s',
        level=logging.DEBUG
    )


def perform_configuration_process(config, directory):
    for section_name, section_config in config.items():
        if 'enabled' not in section_config \
                or section_config['enabled'] not in ('true', 'True', True):
            continue
        if 'module' not in section_config:
            raise Exception('No module specified for configuring %s' % section_name)
        process_section(section_name, section_config, directory)


def process_section(name, config, directory):
    """
    Import the python module which should process this config
    :param name:
    :param config:
    :param directory:
    :return:
    """
    processor = importlib.import_module(name=config['module'])
    processor.process(name, config, directory)


def main():
    try:
        setup_logging()
        directory = internal_configuration.locate_configuration_directory()
        config = internal_configuration.read_internal_configuration()
        perform_configuration_process(config, directory)
        logger.info('Completed')
    except Exception as exception:
        logger.critical(
            'Critical exception occurred',
            exc_info=exception
        )
        exit(1)


if __name__ == "__main__":
    main()

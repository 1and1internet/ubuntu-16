"""
Configurability script

Process which merges custom configuration files and INI files.

"""

import os
import os.path
import logging
import ConfigParser

# noinspection PyUnresolvedReferences
from configurability import custom_files

logger = logging.getLogger(__name__)


def process(name, config, directory):
    """
    Requires the input file (configuration_file_name) in directory to
     be multidimensional representation of overrides for the target file (ini_file_path).

    Input may be any format. Output will always be an ini file.

    :param name: Name of this section of the configuration
    :param config: The configuration dictionary for this section
    :param directory: The directory in which the input files are mounted
    :return:
    """
    for required_key in [
        'ini_file_path',
        'configuration_file_name'
    ]:
        if required_key not in config:
            raise Exception(
                'Required key %s not present in %s section of internal configuration'
                % (name, required_key)
            )
    logger.info('Configuring %s' % name)

    current_values, file_format = custom_files.read_custom_file(config['ini_file_path'])
    custom_values, file_format = custom_files.read_custom_file(
        os.path.join(directory, config['configuration_file_name']))
    resulting_file = ConfigParser.ConfigParser()

    for section_name in set(current_values.keys() + custom_values.keys()):
        resulting_file.add_section(section_name)

    for section_name in current_values.keys():
        if not isinstance(current_values[section_name], dict):
            logger.error('%s is not a valid section in current values' % section_name)
            continue
        for key, value in current_values[section_name].items():
            resulting_file.set(section_name, key, value)

    display_values = {}
    for section_name in custom_values.keys():
        if not isinstance(custom_values[section_name], dict):
            logger.error('%s is not a valid section in custom values' % section_name)
            continue
        for key, value in custom_values[section_name].items():
            display_values['%s/%s' % (section_name, key)] = value
            resulting_file.set(section_name, key, value)
    length = len(max(display_values.keys(), key=len))
    for key in sorted(display_values.keys()):
        logger.info('%s = %s' % (key.rjust(length, ' '), display_values[key]))

    logger.info('Writing %s' % config['ini_file_path'])
    with open(config['ini_file_path'], 'wb') as file_handle:
        resulting_file.write(file_handle)

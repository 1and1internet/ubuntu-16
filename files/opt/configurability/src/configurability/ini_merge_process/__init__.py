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


# noinspection PyBroadException,PyUnboundLocalVariable
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
                % (required_key, name)
            )
    logger.info('Configuring %s' % name)

    error_occurred_while_reading_an_input_file = False

    try:
        current_values, file_format = custom_files.read_custom_file(
            config['ini_file_path']
        )
    except Exception as file_reading_exception:
        logger.error(str(file_reading_exception))  # don't log the full stack trace
        error_occurred_while_reading_an_input_file = True

    try:
        custom_values, file_format = custom_files.read_custom_file(
            os.path.join(directory, config['configuration_file_name'])
        )
    except Exception as file_reading_exception:
        logger.error(str(file_reading_exception))  # don't log the full stack trace
        error_occurred_while_reading_an_input_file = True

    if error_occurred_while_reading_an_input_file:
        logger.info('Not configuring %s (not a critical failure)' % name)
        return  # abort but don't fail

    assert custom_values is not None and isinstance(current_values, dict)
    assert custom_values is not None and isinstance(custom_values, dict)

    resulting_file = ConfigParser.ConfigParser(allow_no_value=True)

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
            if isinstance(value, list) and len(value) == 1:
                # because otherwise mysql gets "sql_mode = [u'NO_ENGINE_SUBSTITUTION']" and barfs.
                # yes it's nasty. yes it shouldn't occur in the first place.
                value = value[0]
            display_values['%s/%s' % (section_name, key)] = value
            resulting_file.set(section_name, key, value)
    length = len(max(display_values.keys(), key=len))
    for key in sorted(display_values.keys()):
        logger.info('%s = %s' % (key.rjust(length, ' '), display_values[key]))

    logger.info('Writing %s' % config['ini_file_path'])
    with open(config['ini_file_path'], 'wb') as file_handle:
        resulting_file.write(file_handle)

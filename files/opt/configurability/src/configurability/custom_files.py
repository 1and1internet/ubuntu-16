"""
Configurability script

Methods used for reading and parsing files.

 -==========================================================================-
    Written for python 2.7 because it is included with Ubuntu 16.04 and I
      wanted to avoid requiring that python 3 also be installed.
 -==========================================================================-
"""

import os
import os.path
import logging
import ConfigParser
import StringIO

logger = logging.getLogger(__name__)


def parse_file_as_ini(file_contents):
    class ExtendedConfigParser(ConfigParser.ConfigParser):
        def read_string(self, data):
            self.readfp(StringIO.StringIO(data))

        # Credit to http://stackoverflow.com/a/3220891
        def as_dict(self):
            d = dict(self._sections)
            for k in d:
                d[k] = dict(self._defaults, **d[k])
                d[k].pop('__name__', None)
            return d

    parser = ExtendedConfigParser(allow_no_value=True)
    parser.read_string(file_contents)
    decoded_data = parser.as_dict()
    if len(decoded_data) == 0:
        raise ValueError
    return decoded_data


def parse_file_as_env(file_contents):
    decoded_data = {}
    lines = file_contents.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name, value = line.split('=', 1)
        name, value = name.strip(), value.strip()
        decoded_data[name] = value
    if len(decoded_data) <= 0:
        raise Exception('No values to load')
    return decoded_data


def parse_file_as_json(file_contents):
    import json
    return json.loads(file_contents)


def parse_file_as_yaml(file_contents):
    import yaml
    return yaml.load(file_contents)


def read_custom_file(file_path):
    logger.info('Reading %s' % file_path)
    with open(file_path) as data_file:
        file_contents = data_file.read()
    parsers = {
        'ini': parse_file_as_ini,
        'env': parse_file_as_env,
        'json': parse_file_as_json,
        'yaml': parse_file_as_yaml
    }
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension[1:]  # Remove the proceeding dot
    if file_extension == '.yml':
        file_extension = '.yaml'
    if file_extension in parsers:
        try:
            return parsers[file_extension](file_contents), file_extension
        except Exception as parse_exception:
            logger.warning(
                '%s does not parse as %s' % (file_path, file_extension),
                exc_info=parse_exception
            )
    for file_format, file_parser in parsers.items():
        # noinspection PyBroadException
        try:
            return file_parser(file_contents), file_format
        except Exception:
            logger.debug('%s does not parse as %s' % (file_path, file_format))
    raise Exception('Unable to parse file: %s' % file_path)

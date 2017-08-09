"""
Configurability script

This script is the bridge in an abstraction layer that sits between our web
 based frontend, and this image/container. It has the responsibility of
 altering the configuration files within this image based on the custom
 configuration files which are mounted into our file system.

There are several inputs to this script.

> Environment Variables are used for platform specific configuration.

> Configuration file within the image is used for image version specific
   configuration, such as locations of files within the image.

> Configuration files mounted in to the container are used for execution
   instance specific settings which need to be honoured.

The following environment variables are supported:

> CONFIGURABILITY_DIR = The directory in which the files are mounted.

 -==========================================================================-
    Written for python 2.7 because it is included with Ubuntu 16.04 and I
      wanted to avoid requiring that python 3 also be installed.
 -==========================================================================-
"""

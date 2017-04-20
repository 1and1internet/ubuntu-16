# Ubuntu 16.04 LTS (Xenial Xerus) Docker Image

This image provides a standard ubuntu docker base image for other docker images to build on top of.

This is created specifically to be run under [OpenShift Origin](https://www.openshift.org/) and [Kubernetes](https://kubernetes.io/). However it is expected to function in any standard Docker environment.

Ensure you specify a user id (UID) other than zero. Running as root is not tested / support a supported configuration.

## Extending this image

You can easily extend the behavour of this image in the following ways

* `/hooks/entrypoint-pre.d/`
  Executables placed in this directory are executed very early on, before anything else is done.

* `/hooks/entrypoint-run`
  If it exists, this is executed if the default command is not overridden. After it's execution completes the default command is executed.

* `/hooks/entrypoint-exec`
  If it exists, this is executed if default command is overridden. After it's execution completes the default command is executed.

* `/hooks/supervisord-pre.d/`
  Executables placed in this directory are executed just before supervisord is executed.

* `/hooks/supervisord-ready`
  If it exists, this is executed once supervisord is read. This is triggered from supervisord itself, when it fires the SUPERVISOR_STATE_CHANGE_RUNNING event.

## Usage

1. Make a Dockerfile and specify `1and1internet/ubuntu-16` on the `FROM` line.
2. Anything you want run in the container should be started by supervisord. 
3. Use a directory called files if you need to copy files in to your new image (see Dockerfile for this image as an example).

## Building and testing

A simple Makefile is included for your convience. It assumes a linux environment with a docker socket avialable at `/var/run/docker.sock`

To build and test just run `make`.
You can also just `make pull`, `make build` and `make test` separately.

Please see the top of the Makefile for various variables which you may choose to customise. Variables may be passed as arguments, e.g. `make IMAGE_NAME=bob` or `make build BUILD_ARGS="--rm --no-cache"`



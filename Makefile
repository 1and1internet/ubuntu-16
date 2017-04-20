PWD = $(shell pwd)
IMAGE_NAME = $(shell basename ${PWD})
BASE_IMAGE = $(shell grep Dockerfile -e FROM | cut -d ' ' -f 2)
RSPEC_IMAGE = 1and1internet/ubuntu-16-rspec
TESTS_REPO = https://github.com/1and1internet/drone-tests.git
DOCKER_SOCKET = /var/run/docker.sock
BUILD_ARGS = --rm
RSPEC_ARGS = 

# To use a locally modified copy of the tests repository set the TESTS_LOCAL variable to the absolute path of where it is located.
TESTS_LOCAL =

all: pull build test

pull:
	##
	## Pulling image updates from registry
	##
	docker pull ${BASE_IMAGE}
	docker pull ${RSPEC_IMAGE}

build:
	##
	## Starting build of image ${IMAGE_NAME}
	##
	docker build ${BUILD_ARGS} --tag ${IMAGE_NAME} .

test:
	##
	## Starting tests inside a new container running ${RSPEC_IMAGE}
ifdef TESTS_LOCAL
	##  with tests from ${TESTS_LOCAL}
	##
	docker run --rm -i -t -v ${DOCKER_SOCKET}:/var/run/docker.sock -v ${PWD}/:/mnt/ -v ${TESTS_LOCAL}/:/drone-tests/ ${RSPEC_IMAGE} make run-rspec IMAGE_NAME=${IMAGE_NAME}
else
	##  with tests from ${TESTS_REPO}
	##
	docker run --rm -i -t -v ${DOCKER_SOCKET}:/var/run/docker.sock -v ${PWD}/:/mnt/ ${RSPEC_IMAGE} make do-test IMAGE_NAME=${IMAGE_NAME}
endif

do-test: checkout-drone-tests run-rspec

checkout-drone-tests:
	mkdir ../drone-tests
	git clone ${TESTS_REPO} ../drone-tests

run-rspec:
	## Testing image ${IMAGE_NAME}
	IMAGE=${IMAGE_NAME} rspec ${RSPEC_ARGS}

.PHONY: all pull build test do-test checkout-drone-tests run-rspec

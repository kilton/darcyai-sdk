#!/bin/bash
#
# check.bash - Checks Darcy AI development environment prerequisites
#

# Check python version
function check_python_version() {

    if ! python3 -c 'import sys; assert sys.version_info >= (3,7)' > /dev/null; then
        echo "ERROR: Darcy AI requires Python 3.7 or later"
        exit 1
    fi

}

# Check OpenCV version
function check_opencv_version() {

    if ! python3 -c 'import cv2; assert cv2.__version__ >= "4.5"' > /dev/null; then
        echo "ERROR: OpenCV 4.5 or later is required"
        exit 1
    fi

}

# Check python package installed
function check_python_package() {

    if ! python3 -c "import $1" > /dev/null; then
        echo "ERROR: Python package '$1' is required"
        exit 1
    fi

}

# Check command exists
function check_command_exists() {

    if ! command -v $1 > /dev/null; then
        echo "ERROR: $1 is required"
        exit 1
    fi

}

check_command_exists python3
check_python_version

check_command_exists docker

check_python_package cv2
check_opencv_version

check_python_package pycoral
check_python_package darcyai

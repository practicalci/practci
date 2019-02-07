#!/bin/bash

# this script is meant to test propagation of errors from the toolchain to the tool

(>&2 echo -n "I am a master error!")
exit -1

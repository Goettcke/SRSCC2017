#!/bin/bash

set -o xtrace

rm -f *.pyc
rm -rf *.zip
rm -f slurm-dump/*
rm -rf output*sample
mkdir -p stash
mv output* stash
rm -rf stash/output*

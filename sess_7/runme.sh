#!/bin/bash
if [ $# == 1 ]; then
    /usr/bin/python3 runner.py $1
else
    echo "Usage $0 [file]"
fi
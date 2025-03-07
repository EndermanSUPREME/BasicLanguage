#!/bin/bash
echo '------ Starting Tests -----'
python3 tokenizer.py && \
python3 parser.py && \
python3 evaluator.py && \
python3 runner.py && \
echo '---- All Tests Passed! ----'

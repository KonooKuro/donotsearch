#!/bin/sh

# 1. Change directory to the *source* directory.
# This makes 'server.py' the root module and solves the
# 'server is not a package' error.
cd /app/server/src

# 2. Run pytest from here.
# We point back to the test files in the parent 'test' folder.
# We tell coverage to measure the current directory ('.').
pytest \
    --cov=. \
    --cov-report=html \
    ../test/test_api.py \
    ../test/test_watermark_coverage.py

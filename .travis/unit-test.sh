#!/bin/bash

set -e
errors=0

# Run unit tests
python barcode_analysis/barcode_analysis_test.py || {
    echo "'python python/barcode_analysis/barcode_analysis_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E barcode_analysis/*.py || {
    echo 'pylint -E barcode_analysis/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"

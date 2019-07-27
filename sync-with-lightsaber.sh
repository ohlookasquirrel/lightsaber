#!/bin/bash

main() {
    if [ -d "/Volumes/CIRCUITPY" ]; then
        find . -maxdepth 1 -not -name "test_*" -name "*.py" -print0 | xargs -0 -I{} cp {} /Volumes/CIRCUITPY
        echo "The feather is on the wind."
    else
        echo "There is no feather."
    fi
}

main "$@"



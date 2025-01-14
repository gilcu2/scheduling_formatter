#!/usr/bin/env sh

TO_CHECK="
src/
tests/
"

flake8 $TO_CHECK


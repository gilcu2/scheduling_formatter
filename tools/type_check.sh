#!/usr/bin/env sh

TO_CHECK="
  src/
  tests/
"

mypy "$TO_CHECK"

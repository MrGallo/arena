#!/bin/bash
pycodestyle arena --ignore=E501,W293
mypy arena --strict

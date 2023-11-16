#!/bin/bash
pycodestyle arena --ignore=E501
mypy arena --strict

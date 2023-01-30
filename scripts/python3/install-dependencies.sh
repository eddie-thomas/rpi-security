#!/bin/bash -

#
# Copyright © 2018 - 2023 by Edward K Thomas Jr
# GNU GENERAL PUBLIC LICENSE https://www.gnu.org/licenses/gpl-3.0.en.html
#

# Installs the Python dependencies.

# Exit when any command fails
set -e

if [ -z "$VIRTUAL_ENV" ]
then
  echo 'Attempting to activate your Python virtual environment...'
  if [ -f ./.venv/bin/activate ]; then
    source ./.venv/bin/activate
    echo 'Done'
  elif [ -f ./.venv/Scripts/activate ]; then
    source ./.venv/Scripts/activate
    echo 'Done'
  fi
fi

if [ -z "$VIRTUAL_ENV" ]
then
  echo 'Unable to activate your Python virtual environment.'
  exit 2
fi

# Use python3 command if available, otherwise try python
# NOTE: Be sure to activate the Python virtual environment before trying to
# resolve the python version
set +e
python_cmd=$(which python3 2> /dev/null)
if [ -n "$python_cmd" ]; then
  python_cmd=python3
else
  python_cmd=$(which python 2> /dev/null)
  if [ -n "$python_cmd" ]; then
    python_cmd=python
  fi
fi

# Assert Python version is 3.7+.
python3_minor_version=$($python_cmd --version | sed -n ';s/Python 3\.\([0-9]*\)\(\.[0-9]*\)*.*/\1/p;')
if ! [[ "$python3_minor_version" -ge '7' ]]; then
  echo "Must have Python 3.7+ installed on path! Found $($python_cmd --version)."
  exit 3
fi
set -e

echo
echo 'Install Python dependencies...'
$python_cmd -m pip install --upgrade pip
$python_cmd -m pip install -r ./scripts/python3/requirements.txt
echo 'Done'

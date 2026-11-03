#!/bin/bash
#
# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


STRATEGY_URL=https://raw.githubusercontent.com/fedora-infra/shared/main/liccheck-strategy.ini

trap 'rm -f $TMPFILE $STRATEGY_TMPFILE' EXIT

set -e
set -x

TMPFILE=$(mktemp -t requirements-XXXXXX.txt)
STRATEGY_TMPFILE=$(mktemp -t liccheck-strategy-XXXXXX.ini)

curl -o $STRATEGY_TMPFILE $STRATEGY_URL

# Liccheck requires pkg_resources: https://github.com/dhatim/python-license-check/issues/117
poetry run pip install "setuptools<82.0.0"

# Use pip freeze instead of poetry export to avoid version conflicts with multi-version markers in lockfile
# poetry export --with dev --without-hashes -f requirements.txt -o $TMPFILE
poetry run pip freeze --exclude-editable --isolated > $TMPFILE

poetry run liccheck -r $TMPFILE -s $STRATEGY_TMPFILE

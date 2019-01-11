#!/bin/bash
set -e
find puppetdb_exporter -name "*.py" | xargs mypy --ignore-missing-imports --strict --disallow-untyped-defs --disallow-untyped-calls --disallow-incomplete-defs

#!/usr/bin/env bash

set -e
py.test --cov=butler_offline butler_offline

#!/bin/sh
set -ex

gunicorn --print-config src.main:app

exec "$@"

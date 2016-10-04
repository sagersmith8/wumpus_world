#!/bin/sh
set -ex

flake8 ai_graph_color tests
nosetests --with-coverage tests

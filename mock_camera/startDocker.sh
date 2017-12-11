#!/bin/bash

python="python3" # "python3" or "python"

export PYTHONUNBUFFERED=TRUE
set DISPLAY :0

$python mqttCamera.py

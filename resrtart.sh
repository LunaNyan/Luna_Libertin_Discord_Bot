#!/bin/bash

kill -9 $(pgrep -f app.py)
./app.py & disown

#!/bin/bash

kill -9 $(pgrep -f luna_libertin_prod_public.py)
/home/pi/apps/luna_libertin/prod_public/luna_libertin_prod_public.py & disown

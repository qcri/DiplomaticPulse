#!/bin/bash

# turn on bash's job control
set -m

# start scrapyd in the background
scrapyd --pidfile= &

# deploy diplomaticpulse to scrapyd
scrapyd-deploy

# bring scrapyd back to foreground
fg %1

#!/bin/sh
PIPE=/tmp/espokseman.$$.wav
mkfifo $PIPE
lame $PIPE - &
espeak -v en-us -w $PIPE
rm $PIPE

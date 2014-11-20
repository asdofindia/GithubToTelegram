#!/bin/zsh

# This file is GPL v3. 

# This script does the task of invoking tg-cli with the right arguments
# You need to edit two things here: the TGDIR and the -p argument value
# Refer README.md for more

TGDIR="/home/akshay/Documents/tech/applications/tg"
RANDFILE=$RANDOM
echo $2 > $RANDFILE
echo "send_text $1 $RANDFILE" | $TGDIR/bin/telegram-cli -W -D -k $TGDIR/server.pub -c $TGDIR/config.sample -p kl
rm -f $RANDFILE

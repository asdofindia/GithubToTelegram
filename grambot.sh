#!/bin/zsh

# This file is GPL v3. 

# This script does the task of invoking tg-cli with the right arguments
# You need to edit two things here: the TGDIR and the -p argument value
# Refer README.md for more

# The directory in which tg-cli is stored. Edit this
TGDIR="/home/akshay/Documents/tech/applications/tg"

RANDFILE=$RANDOM
echo $2 > $RANDFILE

# Remove the "-p kl" if you don't want a separate profile for the bot.
# Otherwise, create a profile named kl, or change kl to your profile name
# The profile need to be saved in config.sample in tg-cli directory
echo "send_text $1 $RANDFILE" | $TGDIR/bin/telegram-cli -W -D -k $TGDIR/server.pub -c $TGDIR/config.sample -p kl

rm -f $RANDFILE

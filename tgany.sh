#!/bin/zsh
pwd
TGCLI="/home/akshay/Documents/tech/applications/tg-kn/bin/telegram-cli"
RANDFILE=$RANDOM
echo $2 > $RANDFILE
echo "send_text $1 $RANDFILE" | $TGCLI -W -D -k server.pub
rm -f $RANDFILE
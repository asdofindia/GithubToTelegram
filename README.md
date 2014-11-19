#Github To Telegram #

A script that uses PyGithub to poll the Github api and send interesting events to your favorite group via Telegram-CLI

###Requirements###
It's currently written in python3 (only because I hate unicode encoding errors). But it's easily portable to python2, just change the print functions. Otherwise install python3

    sudo apt-get install python3

For calling Github API we use PyGithub

	sudo easy_install3 PyGithub

And of course, you need the quintessential [tg-cli](https://github.com/vysheng/tg). 

    Follow [vysheng/tg/#installation](https://github.com/vysheng/tg/#installation)

### Edits to make ###

* Rename config.sample.py to config.py. `mv config.sample.py config.py`
* Modify your github username and password
* Modify the group you want it sent to
* Edit `tgany.sh`. Put the location of tg-cli where I have put my location. If you use bash instead of zsh, you may have to change the magic hashbang in the first line to `#!/bin/sh` 
* Edit `gitbot.py`. Change `DELTATIME=330` to the difference between your timezone and UTC in minutes. IST = +0530, so 5*60+30=330

### Run ###

    python3 gitbot.py


### Files explained ###
config is to store username and password without accidentally committing to github.

gitbot is the script.

A lastpoll file will be generated which contains pickled object of the last polls made

server.pub is the telegram server's public key. This is just copy pasted from tg-cli so that it's easier to type the path inside tgany.sh

tgany.sh is a bash script which takes two arguments - a to address, and a message - and calls the tg-cli with the right settings  

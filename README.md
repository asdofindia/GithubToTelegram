#Github To Telegram #

A script that uses PyGithub to poll the Github api and send interesting events to your favorite group via Telegram-CLI

###Requirements###
It's currently written in python3 (only because I hate unicode encoding errors). But it's easily portable to python2, just change the print functions. Otherwise install python3

* `sudo apt-get install python3`

And of course, you need the quintessential [tg-cli](https://github.com/vysheng/tg). 

* Follow [vysheng/tg/#installation](https://github.com/vysheng/tg/#installation)

### Edits to make ###

* Rename config.sample.py to config.py. `mv config.sample.py config.py`
* In `config.py` Modify your github username and password
* Modify the chat name you want messages sent to
* Modify the apps you want to track on github
* Edit `grambot.sh`. Put the directory of tg-cli where TGDIR is assigned. Avoid trailing slash. If you use bash instead of zsh, you may have to change the magic hashbang in the first line to `#!/bin/sh` 
* Within your tg-cli installation, you need to edit the `config.sample` to create a profile for the bot. Refer [this file](https://github.com/vysheng/tg/blob/master/config.sample). If you don't want to do this, just remove "-p kl" from grambot.sh

### Run ###

    python3 gitbotnew.py


### Files explained ###
config is to store username and password without accidentally committing to github.

gitbotnew is the script.

The data directory contains the essential etags and stuff that makes github API work without polling too much

server.pub is the telegram server's public key. This is just copy pasted from tg-cli so that it's easier to type the path inside tgany.sh

grambot.sh is a bash script which takes two arguments - a to address, and a message - and calls the tg-cli with the right settings  


# License #
All the stuff is GPL v3. Edit it, share it, but don't sell it.
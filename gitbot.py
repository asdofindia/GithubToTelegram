#!/usr/bin/python3

from github import Github
import pickle
import time
import datetime
import subprocess
import socket
import traceback
import config

appslist = ["android", "webogram", "tg-cli", "Tsupport (Android)", "TDesktop"]

# required to adjust the time zone. India is +0530, so 330 minutes have to
# be subtracted from datetime.now() to match API server
DELTATIME = 330


def getlasttime():
    try:
        with open('lastpoll', 'rb') as lastpoll:
            lasttimes = pickle.load(lastpoll)
    except FileNotFoundError:
        print(
            "appears like you haven't checked ever. How many minutes back in time do you want to go? ")
        minutes = int(input())
        if minutes < DELTATIME:
            minutes += DELTATIME
        with open('lastpoll', 'wb') as lastpoll:
            lasttime = datetime.datetime.now() - \
                datetime.timedelta(minutes=minutes)
            lasttimes = dict(zip(appslist, [
                             dict(zip(["commits", "issues", "comments"], [lasttime] * 3))] * len(appslist)))
            print("created lasttimes, ", lasttimes)
            pickle.dump(lasttimes, lastpoll)
    return lasttimes


def sendtotg(message):
    togroup = "TSF_Chat_(unofficial)"
    if config.togroup:
        togroup = config.togroup
    subprocess.Popen(['./tgany.sh', togroup, message])

g = Github(config.username, config.password)
# zhukov=g.get_user('zhukov')
# webogram=zhukov.get_repo('webogram')
webogram = g.get_repo(15652312)
# drklo=g.get_user('drklo')
# drklo.get_repo('Telegram')
android = g.get_repo(13862381)
# vysh=g.get_user("vysheng")
# cli=vysh.get_repo("tg")
cli = g.get_repo(13297858)
# rubenlagus/tsupport
tsupand = g.get_repo(22311913)
# telegramdesktop/tdesktop
tdesk = g.get_repo(19374812)
# asdofindia/try_git
test = g.get_repo(8390629)
branches = [[android, "dev"], [webogram, "master"],
            [cli, "master"], [tsupand, "dev"], [tdesk, "master"]]
apps = dict(zip(appslist, branches))
while True:
    lasttimes = getlasttime()
    print ("polling")

    try:
        for app in apps:
            lasttime = lasttimes[app]["commits"]
            print ("polling", app, "since", repr(lasttime))
            newlasttime = datetime.datetime.now(
            ) - datetime.timedelta(minutes=DELTATIME)
            for commit in apps[app][0].get_commits(since=lasttime, sha=apps[app][1]).reversed:
                output = "".join(
                    [commit.commit.message, '\n~ ', commit.commit.author.name, ' on ', app, '\nRead more at: ', commit.html_url])
                print(output)
                sendtotg(output)
            lasttimes[app]["commits"] = newlasttime
            with open('lastpoll', 'wb') as lastpoll:
                pickle.dump(lasttimes, lastpoll)

        for app in apps:
            lasttime = lasttimes[app]["issues"]
            print ("polling", app, "since", repr(lasttime))
            newlasttime = datetime.datetime.now(
            ) - datetime.timedelta(minutes=DELTATIME)
            for issue in apps[app][0].get_issues(since=lasttime).reversed:
                output = "".join(
                    [app, ':\n"', issue.title, '"\n', issue.body, '\n~', issue.user.login, '\n', issue.html_url])
                print(output)
                sendtotg(output)
            lasttimes[app]["issues"] = newlasttime
            with open('lastpoll', 'wb') as lastpoll:
                pickle.dump(lasttimes, lastpoll)

        for app in apps:
            lasttime = lasttimes[app]["comments"]
            print ("polling", app, "since", repr(lasttime))
            newlasttime = datetime.datetime.now(
            ) - datetime.timedelta(minutes=DELTATIME)
            for comment in apps[app][0].get_issues_comments(since=lasttime).reversed:
                output = "".join(
                    [app, ' issue comment:\n', comment.body, '\n~', comment.user.login, '\n', comment.html_url])
                print(output)
                sendtotg(output)
            lasttimes[app]["comments"] = newlasttime
            with open('lastpoll', 'wb') as lastpoll:
                pickle.dump(lasttimes, lastpoll)

    except socket.gaierror:
        print("socket error. Ignoring")

    except socket.timeout:
        print("socket timeout")

    except TypeError:
        print ("type error")
        print (traceback.format_exc())

    print("going to sleep")
    time.sleep(120)

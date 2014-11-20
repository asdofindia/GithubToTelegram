#!/bin/python3

import requests
import config
import time
import subprocess
import os
import pickle


class Bot(object):

    """docstring for Bot
    Basically we are going to connect the bot
    """

    def __init__(self):
        super(Bot, self).__init__()
        #self.arg = arg
        self.username = config.username
        self.password = config.password
        self.auth = (self.username, self.password)
        self.headers = {"Accept": "application/vnd.github.v3+json",
                        "User-Agent":
                        "asdofindia's githubtotelegram bot script"}
        self.apps = config.apps

    def poll(self, endpoint, headers, payload):
        response = requests.get(
            'https://api.github.com' + endpoint,
            headers=headers, params=payload, auth=self.auth)
        return response

    def getissue(self, apiend):
        response = requests.get(apiend, auth=self.auth)
        return response.json()['title']

    def createargs(self, appname, app):
        owner = app["owner"]
        repo = app["repo"]
        branch = app["branch"]
        commitsendpoint = "/repos/%s/%s/commits" % (owner, repo)
        issuesendpoint = "/repos/%s/%s/issues" % (owner, repo)
        commentsendpoint = "/repos/%s/%s/issues/comments" % (owner, repo)
        commitsheaders = {
            "If-None-Match": self.getconfig(appname, "commits") or "0"}
        issuesheaders = {
            "If-None-Match": self.getconfig(appname, "issues") or "0"}
        commentsheaders = {
            "If-None-Match": self.getconfig(appname, "comments") or "0"}
        commitspayload = {"sha": branch}
        issuespayload = {}
        commentspayload = {"sort": "created", "direction": "desc"}
        commits = [commitsendpoint, commitsheaders, commitspayload]
        issues = [issuesendpoint, issuesheaders, issuespayload]
        comments = [commentsendpoint, commentsheaders, commentspayload]

        return commits, issues, comments

    def getconfig(self, appname, kind):
        depickled = self.depickle(os.path.join("data", appname, kind))
        return depickled

    def depickle(self, path):
        try:
            with open(path, 'rb') as pickled:
                depickled = pickle.load(pickled)
            return depickled
        except FileNotFoundError:
            print(path)
            print("Never created file.")
            return None

    def setconfig(self, appname, kind, content):
        return self.dopickle(os.path.join("data", appname, kind), content)

    def dopickle(self, path, content):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, 'wb') as topickle:
            pickle.dump(content, topickle)

    def controller(self):
        for app in self.apps:
            commits, issues, comments = self.createargs(app, self.apps[app])
            self.processcommits(self.poll(*commits), app)
            self.processissues(self.poll(*issues), app)
            self.processcomments(self.poll(*comments), app)

    def processcommits(self, response, app):
        if not response.status_code == 200:
            return
        lastcommitsha = self.getconfig(app, "commitssha") or None
        if lastcommitsha:
            indextostart = None
            for index, commit in enumerate(response.json()):
                if commit['sha'] == lastcommitsha:
                    indextostart = index - 1
            if indextostart:
                index = indextostart
                while index >= 0:
                    commit = response.json()[index]
                    tosend = "%s updated:\n%s\n~%s" % (
                        app, commit['commit']['message'], commit['html_url'])
                    self.sendtotg(tosend)
                    self.setconfig(
                        app, "commitssha", response.json()[index]['sha'])
                    index -= 1
        else:
            self.setconfig(app, "commitssha", response.json()[0]['sha'])
        self.setconfig(app, "commits", response.headers['etag'])

    def processissues(self, response, app):
        if not response.status_code == 200:
            return
        lastissuesid = self.getconfig(app, "issuesid") or None
        if lastissuesid:
            indextostart = None
            for index, issue in enumerate(response.json()):
                if issue['id'] == lastissuesid:
                    indextostart = index - 1
            if indextostart:
                index = indextostart
                while index >= 0:
                    issue = response.json()[index]
                    tosend = "%s created an issue: [%s]%s\n\n %s\n~%s" % (
                        issue['user']['login'], app, issue['title'],
                        issue['body'], issue['html_url'])
                    self.sendtotg(tosend)
                    self.setconfig(
                        app, "issuesid", response.json()[index]['id'])
                    index -= 1
        else:
            self.setconfig(app, "issuesid", response.json()[0]['id'])
        self.setconfig(app, "issues", response.headers['etag'])

    def processcomments(self, response, app):
        if not response.status_code == 200:
            return
        lastcommentid = self.getconfig(app, "commentid") or None
        if lastcommentid:
            indextostart = None
            for index, comment in enumerate(response.json()):
                if comment['id'] == lastcommentid:
                    indextostart = index - 1
            if indextostart:
                index = indextostart
                while index >= 0:
                    comment = response.json()[index]
                    tosend = "%s commented on issue: [%s]%s\n\n %s\n~%s" % (
                        comment['user']['login'], app, self.getissue(
                            comment['issue_url']), comment['body'],
                        comment['html_url'])
                    self.sendtotg(tosend)
                    self.setconfig(
                        app, "commentid", response.json()[index]['id'])
                    index -= 1
        else:
            self.setconfig(app, "commentid", response.json()[0]['id'])
            print(response.json()[0]['html_url'])
        self.setconfig(app, "comments", response.headers['etag'])

    def sendtotg(self, message):
        togroup = config.togroup
        subprocess.Popen(['./grambot.sh', togroup, message])

    def start(self):
        self.stopped = False
        while not self.stopped:
            self.controller()
            time.sleep(120)

    def stop(self):
        self.stopped = True
        print("Caught KeyboardInterrupt. Shutting down")


if __name__ == '__main__':
    bot = Bot()
    try:
        bot.start()
    except KeyboardInterrupt:
        bot.stop()

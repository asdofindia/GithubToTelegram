#!/bin/python3
# move this file to config.py

# you need to save your github username and password
# here so that maximum api calls can be made

username = "superman"
password = "krypton"

# Remember, tg-cli wants to replace spaces with underscores
togroup = "Xenonites_rock_the_world"

shortenurl=False


# add the apps you want to track here, in the following format
# "<anyname>" : {"owner": "<ownername>",
#                "repo": "<reponame>", "branch" : "<branch to track"}
apps = {
    "cometlander": {"owner": "superman", "repo": "philae", "branch": "dev"},
    "spacecraft": {"owner": "esa", "repo": "rosetta", "branch": "stable"}
}

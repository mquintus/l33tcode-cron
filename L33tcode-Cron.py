#########################################
#
# Welcome.
# This script is your solution when you need to update your git repo based on the
# **l33tcode daily challenge**
#
# It helps you to:
# - Fetch a repository from github
# - Update files according to patterns in relation to the l33tcode daily challenge
# - Commit & Push to github
#
# Todo:
# - Creating Issues
# - Creating Pull Requests

import yaml
import os
import subprocess
import re
import logging

from src.DailyChallengeLib import DailyChallengeLib
from src.UseLeetcodeInfoToUpdateFiles import UseLeetcodeInfoToUpdateFiles

def check_git_repo(repo):
    # Regex to check valid Git Repository
    regex = "((http|git|ssh|http(s)|file|\/?)"\
    "|(git@[\w\.]+))(:(\/\/)?)([\w\.@\:/\-~]+)(\.git)(\/)?"
    p = re.compile(regex)
    # If the string is empty
    # return False
    if (repo is None or repo == None or len(repo) == 0):
        return False
    return re.search(p, repo)

def main(configFileHandle):

    dailyChallengeLib = DailyChallengeLib()
    data = dailyChallengeLib.retrieve()

    config = yaml.safe_load(configFileHandle)
    if not 'repo' in config:
        raise(Exception("Config must provide 'repo' value to check out before continuing."))

    if not check_git_repo(config['repo']):
        raise(Exception("Invalid git repo " + config['repo']))

    if os.path.exists("tmprepo"):
        subprocess.run(["rm", "-rf", "tmprepo"], check=True)
    subprocess.run(["git", "clone", config['repo'], "tmprepo"], check=True)
    useLeetcodeInfoToUpdateFiles = UseLeetcodeInfoToUpdateFiles()
    if 'append' in config:
        for adjust in config['append']:
            logging.warning(adjust)
            useLeetcodeInfoToUpdateFiles.adjustFile(
                data,
                "tmprepo/" + adjust['file'],
                adjust['match'],
                adjust['append'],
            )
    if 'prepend' in config:
        for adjust in config['prepend']:
            logging.warning(adjust)
            useLeetcodeInfoToUpdateFiles.adjustFile(
                data,
                "tmprepo/" + adjust['file'],
                adjust['match'],
                adjust['prepend'],
            )
    if 'replace' in config:
        for adjust in config['replace']:
            logging.warning(adjust)
            useLeetcodeInfoToUpdateFiles.adjustFile(
                data,
                "tmprepo/" + adjust['file'],
                adjust['matchbegin'],
                adjust['matchend'],
                adjust['replace'],
            )
    if 'create' in config:
        for create in config['create']:
            logging.warning(create)
            useLeetcodeInfoToUpdateFiles.createFile(
                data,
                "tmprepo/" + create['file'],
                create['insert'],
            )
    commitmsg = useLeetcodeInfoToUpdateFiles.enhance(data, config['commitmsg'])
    subprocess.run(["git", "add", "."], cwd="tmprepo", check=True)
    subprocess.run(["git", "commit", "-m", f"'{commitmsg}'"], cwd="tmprepo", check=True)
    subprocess.run(["git", "push"], cwd="tmprepo", check=True)
    #subprocess.run(["rm", "-rf", "tmprepo"], check=True)


# l33tcode-reload
configFileHandle = open("l33tcode-reload.config")
main(configFileHandle)
configFileHandle.close()

# l33tcode-testcase-generator
#configFileHandle = open("l33tcode-testcase-generator.config")
#main(configFileHandle)
#configFileHandle.close()

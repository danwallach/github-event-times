# github-event-times.py
# Dan Wallach <dwallach@rice.edu>

import requests
import json
import re
import time
import argparse
import pprint

# see installation and usage instructions in README.md

defaultGithubToken = "YOUR_TOKEN_HERE"

# and we're going to need the name of your GitHub "project" in which all your
# students' work lives.

# Example: for https://github.com/RiceComp215/comp215-2017-week08-operations-username,
# you might set defaultGithubProject to "RiceComp215"
defaultGithubProject = "YOUR_PROJECT_HERE"

# command-line argument processing

parser = argparse.ArgumentParser(description='Get event timestamps from a GitHub repo.')
parser.add_argument('--token',
                        nargs='?',
                        default=defaultGithubToken,
                        help='GitHub API token')
parser.add_argument('--project',
                        nargs='?',
                        default=defaultGithubProject,
                        help='GitHub project to scan, default: ' + defaultGithubProject)
parser.add_argument('repo',
                        nargs='+',
                        default="",
                        help='repo to query, no default')

args = parser.parse_args()

githubRepos = args.repo
githubProject = args.project
githubToken = args.token

requestHeaders = {
    "User-Agent": "GitHubEventTimes/1.0",
    "Authorization": "token " + githubToken,
}

pp = pprint.PrettyPrinter(indent=2)

for repo in githubRepos:
    response = requests.get('https://api.github.com/repos/%s/%s/events' % (githubProject, repo), headers = requestHeaders)

    if response.status_code != 200:
        print "Error in request: " + response.json()
        exit(1)

    eventList = [x for x in response.json() if x['type'] == 'PushEvent']  # we don't care about other event types

    # Each push event looks like this:
    # { u'actor': { u'avatar_url': u'https://avatars.githubusercontent.com/u/11111111?',
    #               u'display_login': u'username',
    #               u'gravatar_id': u'',
    #               u'id': 11111111,
    #               u'login': u'username',
    #               u'url': u'https://api.github.com/users/username'},
    #   u'created_at': u'2017-10-23T22:36:39Z',
    #   u'id': u'3333333333',
    #   u'org': { u'avatar_url': u'https://avatars.githubusercontent.com/u/11111111?',
    #             u'gravatar_id': u'',
    #             u'id': 22222222,
    #             u'login': u'RiceComp215',
    #             u'url': u'https://api.github.com/orgs/RiceComp215'},
    #   u'payload': { u'before': u'1212121212121212121212121211212121212121',
    #                 u'commits': [ { u'author': { u'email': u'username@rice.edu',
    #                                              u'name': u'Student Name'},
    #                                 u'distinct': True,
    #                                 u'message': u'commit message here',
    #                                 u'sha': u'2323232323232323233223233233232323232223',
    #                                 u'url': u'https://api.github.com/repos/RiceComp215/comp215-2017-week08-operations-username/commits/2323232323232323233223233233232323232223'}],
    #                 u'distinct_size': 1,
    #                 u'head': u'2323232323232323233223233233232323232223',
    #                 u'push_id': 4444444444,
    #                 u'ref': u'refs/heads/master',
    #                 u'size': 1},
    #   u'public': False,
    #   u'repo': { u'id': 555555555,
    #              u'name': u'RiceComp215/comp215-2017-week08-operations-username',
    #              u'url': u'https://api.github.com/repos/RiceComp215/comp215-2017-week08-operations-username'},
    #   u'type': u'PushEvent'}

    print "Events for " + repo
    print
    print "\\begin{tabular}{lll}"
    print "{\\bf Commit ID} & {\\bf Comment} & {\\bf GitHub push time} \\\\" 
    print "\\hline"
    for event in eventList:
        try:
            date = event['created_at']
            commits = event['payload']['commits']
            for commit in commits:
                commitMessage = commit['message']
                commitHash = commit['sha'][0:7] # only the first 7 characters, consistent with how GitHub reports commitIDs on its web front-end
                print "%s & %s & %s \\\\" % (commitHash, commitMessage, date)
        except KeyError:
            print "Error: malformed event!"
            pp.pprint(event)
    print "\\hline"
    print "\\end{tabular}"
    print

# github-event-times.py
# Dan Wallach <dwallach@rice.edu>

import requests
import json
import re
import time
import argparse
import pprint

# see installation and usage instructions in README.md

defaultGithubToken = ["YOUR_TOKEN_HERE"]

# and we're going to need the name of your GitHub "project" in which all your
# students' work lives.

# Example: for https://github.com/RiceComp215/comp215-2017-week08-operations-username,
# you might set defaultGithubProject to "RiceComp215"
defaultGithubProject = ["YOUR_PROJECT_HERE"]

# command-line argument processing

parser = argparse.ArgumentParser(description='Get event timestamps from a GitHub repo.')
parser.add_argument('--token',
                        nargs=1,
                        default=defaultGithubToken,
                        help='GitHub API token')
parser.add_argument('--project',
                        nargs=1,
                        default=defaultGithubProject,
                        help='GitHub project to scan, default: ' + defaultGithubProject[0])
parser.add_argument('repo',
                        nargs='+',
                        default="",
                        help='repo to query, no default')

args = parser.parse_args()

githubRepos = args.repo
githubProject = args.project[0]
githubToken = args.token[0]

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
                commitMessage = commit['message'].splitlines()[0] # only the first line if multiline
                commitHash = commit['sha'][0:7] # only the first 7 characters, consistent with how GitHub reports commitIDs on its web front-end
                print "%s & %s & %s \\\\" % (commitHash, commitMessage, date)
        except KeyError:
            print "Error: malformed event!"
            pp.pprint(event)
    print "\\hline"
    print "\\end{tabular}"
    print

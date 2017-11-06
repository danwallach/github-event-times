# github-event-times.py 

This program uses the GitHub "Events" API to print all of the *push*
times for each commit, with its output in LaTeX "tabular" format. This
might be useful if you have a student who you suspect of falsifying
commit times around a deadline and you need to document what happened.

## Installation


1) If you haven't already done this, you'll first need to `pip install
requests` for a necessary library.

2) Get a GitHub token with all the "Repo" privileges. You do
this on the GitHub website
[(instructions)](https://github.com/blog/1509-personal-api-tokens). 

3) Optionally, edit the `defautGithubProject` variable to reflect your
   project's name (e.g., for `https://github.com/RiceComp215`, the
   project name is `RiceComp215`). You can also install your GitHub
   API token in the `defaultGithubToken` variable.

## Usage

Now let's say you want to get the commit times for a series of repos
with
names like assignment3-student1 and assignment3-student2, 
you can simply run `python github-event-times.py assignment3-student1
assignment3-student2`
and it will print a table with the commit IDs (7 digit prefix, same
as reported on GitHub's list of commits), the commit string, and the
time at which that commit was pushed to GitHub. Note that times are
reported in [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) style,
which is UTC, so you may wish to adjust this to your local time.

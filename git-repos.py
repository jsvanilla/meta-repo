""" Collect repository information from GitHub and generate a markdown table.

Usage:
    git-repos.py -h | --help
    git-repos.py --username=<your_username> [--include_private]

Options:
    -h --help                    Display this help message.
    --username=<your_username>   Your GitHub username.
    --include_private            Whether to include private repos. [default: False]
"""
import datetime
from docopt import docopt
from getpass import getpass
from github import Github
import json
import os
import yaml

PROJECTS_HEADER = '## Projects\n'

class Projects:
    status_options = ['Current', "Stale", "Archive"]

    def __init__(self, github, include_private=False):
        """ Store information about a user's github repositories
        :param github: a github object from pygithub
        """
        self.repos = {status: [] for status in self.__class__.status_options}
        user = github.get_user(github.get_user().login)
        for gh_repo in github.get_user().get_repos():
            # only count repositories the user owns or is a collaborator in
            is_owner = gh_repo.owner == user
            is_contributor = user in gh_repo.get_contributors()
            # only include contributing repos and respect privacy preference
            if (is_owner or is_contributor) and (include_private or not gh_repo.private):
                repo = Repo(gh_repo)
                self.repos[repo.status].append(repo)
        for status, repo_list in self.repos.items():
            repo_list.sort(reverse = True, key = lambda repo: repo.last_modified)

    @property
    def markdown_table(self):
        table = [PROJECTS_HEADER]
        for status in self.repos:
            table += [f"\n### {status}\n| Repository | Description | Owner | Language(s) |\n|---|---|---|---|\n"]
            for repo in self.repos[status]:
                table.append(f"| {repo.name} | {repo.description} | {repo.owner} | {repo.languages} |\n")
        return table

class Repo:
    six_months = datetime.timedelta(days=182)

    def __init__(self, repo):
        """ Store information about a github repository
        :param repo: a github repository object from pygithub
        """
        self.owner = f"[{repo.owner.login}]({repo.owner.html_url})"
        self.name = f"[{repo.name}]({repo.url})"
        self.url = repo.clone_url
        self.description = repo.description
        self.languages = ', '.join(repo.get_languages())
        if repo.archived:
            status = "Archive"
        elif (datetime.datetime.now() - repo.updated_at) > self.__class__.six_months:
            status = "Stale"
        else:
            status = "Current"
        assert status in Projects.status_options
        self.status = status
        self.last_modified = repo.updated_at.strftime("%Y-%m-%d")

def main(args):
    password = getpass("Enter your GitHub password: ")
    print("Collecting repo information from GitHub...")
    github = Github(args['--username'], password)
    projects = Projects(github, include_private=args['--include_private'])

    print("Updating the Projects table...")
    with open('README.md', 'r') as file:  # collect everything except the old projects table
        head = [file.readline()]
        line = file.readline()
        while line != PROJECTS_HEADER:
            head.append(line)
            line = file.readline()
        assert line == PROJECTS_HEADER
        line = file.readline()
        while not line.startswith("## "):
            line = file.readline()  # skip stuff under Projects subheading
        tail = ['\n'+line]
        for line in file:
            tail.append(line)

    with open('README.md', 'w') as file:
        file.writelines(head)
        file.writelines(projects.markdown_table)
        file.writelines(tail)

    print("Done!")

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)

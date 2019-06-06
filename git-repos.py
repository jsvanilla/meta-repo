""" Collect repository information from GitHub and generate a markdown table.

Usage:
    git-repos.py -h | --help
    git-repos.py [--username=<your_username> | --token=<path_to_token>] [--include_private]

Options:
    -h --help                       Display this help message.
    -u --username=<your_username>   Your GitHub username.
    -t --token=<path_to_token>      Path to a text file containing your GitHub access toekn.
    --include_private               Whether to include private repos. [default: False]
"""
import datetime
from docopt import docopt
from getpass import getpass
from github import Github
import json
import os
import yaml

PROJECTS_HEADER = '## Projects\n'

class Repos:
    """ Store information about a user's github repositories & generate a markdown table """
    status_options = ['Current', "Stale", "Archive"]

    def __init__(self, github, include_private=False):
        """
        :param github: a github object from pygithub
        :param include_private: whether to include private repositories
        """
        user = github.get_user(github.get_user().login)
        self.repos = {status: [] for status in self.__class__.status_options}
        # iterate over all repos this user has read access to
        for gh_repo in github.get_user().get_repos():
            # only count repositories the user owns or contributes to
            is_owner = gh_repo.owner == user
            is_contributor = user in gh_repo.get_contributors()
            # respect privacy preference
            if (is_owner or is_contributor) and (include_private or not gh_repo.private):
                repo = Repo(gh_repo)
                self.repos[repo.status].append(repo)
        for status, repo_list in self.repos.items():
            repo_list.sort(reverse = True, key = lambda repo: repo.last_modified)
        self.gists = list()
        for gist in github.get_user().get_gists():
            if include_private or gist.public:
                self.gists.append(Gist(gist))
        self.gists.sort(reverse = True, key = lambda gist: gist.last_modified)


    @property
    def markdown_table(self):
        """
        :return: a list containing strings in markdown table format
        """
        table = [PROJECTS_HEADER]

        for status in self.repos:
            table.append(f"\n### {status}\n| Repository | Description | Owner | Language(s) |\n|---|---|---|---|\n")
            for repo in self.repos[status]:
                table.append(repo.markdown)

        table.append(f"\n### Gists\n| Description |\n|---|\n")
        for gist in self.gists:
            table.append(gist.markdown)

        return table

class Repo:
    """ Store info about a github repository """
    six_months = datetime.timedelta(days=182)

    def __init__(self, repo):
        """ Store minimal info about a github repository
        :param repo: a github repository object from pygithub
        """
        self.owner = f"[{repo.owner.login}]({repo.owner.html_url})"
        self.name = f"[{repo.name}]({repo.html_url})"
        self.description = repo.description
        self.languages = ', '.join(repo.get_languages())
        if repo.archived:
            status = "Archive"
        elif (datetime.datetime.now() - repo.updated_at) > self.__class__.six_months:
            status = "Stale"
        else:
            status = "Current"
        assert status in Repos.status_options
        self.status = status
        self.last_modified = repo.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.name} | {self.description} | {self.owner} | {self.languages} |\n"

class Gist:
    def __init__(self, gist):
        """ Store minimal info about a github Gist
        :param gist: a github gist object from pygithub
        """
        self.owner = f"[{gist.owner.login}]({gist.owner.html_url})"
        self.description = f"[{gist.description}]({gist.html_url})"
        self.last_modified = gist.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.description} |\n"


def main(args):
    """
    Collects repositories the user owns or has contributed to
    and updates the Projects table in README.md
    """
    print("Logging into GitHub...")
    if args['--token']:
        with open(args['--token'], 'r') as token_file:
            token = token_file.readline().strip()
        github = Github(token)
    else:
        password = getpass("Enter your GitHub password: ")
        github = Github(args['--username'], password)
    print("Collecting repos & gists...")
    projects = Repos(github, include_private=args['--include_private'])

    print("Updating the Projects table...")
    with open('README.md', 'r') as file:  # collect everything except the old projects table
        head = [file.readline()]
        line = file.readline()
        while line != PROJECTS_HEADER:
            head.append(line)
            line = file.readline()
        assert line == PROJECTS_HEADER
        line = file.readline()
        while not line.startswith("## "):  # TODO: don't loop indefinitely if there's no heading afer Projects
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

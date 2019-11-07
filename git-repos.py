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
import os
from getpass import getpass
from docopt import docopt
from github import Github
import GitHubLangStats


def main(args):
    """
    Collects repositories the user owns or has contributed to
    and updates the Projects table in README.md
    """
    for dir in ("figures",):
        if not os.path.exists(dir):
            os.mkdir(dir)

    github = login(args)
    projects = GitHubLangStats.Repos(github, include_private=args["--include_private"])

    print("Updating the Projects table...")
    with open(
        "README.md", "r"
    ) as file:  # collect everything except the old projects table
        head = [file.readline()]
        line = file.readline()
        while line != projects.PROJECTS_HEADER:
            head.append(line)
            line = file.readline()
        assert line == projects.PROJECTS_HEADER
        line = file.readline()
        while not line.startswith(
            "## "
        ):  # TODO: don't loop indefinitely if there's no heading after Projects
            line = file.readline()  # skip stuff under Projects subheading
        tail = ["\n" + line]
        for line in file:
            tail.append(line)

    with open("README.md", "w") as file:
        file.writelines(head)
        file.writelines(projects.markdown_table)
        file.writelines(tail)

    csv_filename = "repos.csv"
    print(f"Writing {csv_filename}")
    projects.write_csv(csv_filename)

    print("Done!")


def login(args):
    print("Logging into GitHub...")
    if args["--token"]:
        with open(args["--token"], "r") as token_file:
            token = token_file.readline().strip()
        github = Github(token)
    else:
        password = getpass("Enter your GitHub password: ")
        github = Github(args["--username"], password)
    return github


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)

""" Collect repository information from GitHub and generate a markdown table.

Usage:
    git-repos.py -h | --help
    git-repos.py [--username=<your_username> | --token=<string>] [--include_private]

Options:
    -h --help                       Display this help message.
    -u --username=<your_username>   Your GitHub username.
    -t --token=<string>             Your GitHub access token as a string.
    --include_private               Whether to include private repos. [default: False]
"""
from docopt import docopt
import base64
import datetime
from getpass import getpass
from github import Github
import json
import pandas as pd


def main(args):
    """
    Collects repositories the user owns or has contributed to
    and updates the Projects table in README.md
    """
    github = login(username=args["--username"], token=args["--token"])
    projects = Projects(github, include_private=args["--include_private"])
    projects.write_csv()
    projects.write_markdown()
    print("Done!")


def login(username=None, token=None):
    print("Logging into GitHub...")
    if token:
        github = Github(token)
    elif username:
        password = getpass("Enter your GitHub password: ")
        github = Github(username, password)
    else:
        raise ValueError("Must define either token or username to login to GitHub")
    return github


class Projects:
    """ Handle information about a user's github repositories, gists, & languages """

    status_options = ["Current", "Stale", "Archive"]

    PROJECTS_HEADER = "## Projects\n"

    def __init__(self, github, include_private=False):
        """
        :param github: a github object from pygithub
        :param include_private: whether to include private repositories
        """
        self.data = pd.DataFrame(
            columns=[
                "language",
                "language_repo_bytes",
                "repo_name",
                "repo_url",
                "repo_owner_name",
                "repo_owner_url",
                "repo_last_updated_date",
                "repo_description",
            ]
        )
        self.repos = {status: [] for status in self.__class__.status_options}
        self._get_repos(github, include_private)
        self.gists = list()
        self._get_gists(github, include_private)

    @classmethod
    def from_token(cls, token):
        return cls(login(token=token))

    @classmethod
    def from_username(cls, username):
        return cls(login(username=username))

    def _get_repos(self, github, include_private=False):
        print("Collecting repos:")
        user = github.get_user(github.get_user().login)
        prev_repo_owner = ""
        # iterate over all repos this user has read access to
        for gh_repo in github.get_user().get_repos():
            if prev_repo_owner != gh_repo.owner.login:
                prev_repo_owner = gh_repo.owner.login
                print(f"\t{prev_repo_owner}")
            # only count repositories the user owns or contributes to
            is_owner = gh_repo.owner == user
            is_contributor = user in gh_repo.get_contributors()
            if is_owner or is_contributor:
                print(f"\t\t{gh_repo.name}")
                languages = (
                    gh_repo.get_languages()
                )  # excludes vendor languages from the repo's .gitattributes
                if languages:
                    print(
                        f"\t\t\t{sorted(languages.keys(), key=lambda k: languages[k], reverse=True)}"
                    )
                    for (
                        language,
                        bytes_count,
                    ) in (
                        languages.items()
                    ):  # get bytes counts for all languages for all repos
                        if language == "Jupyter Notebook":
                            bytes_count = count_jupyter_bytes(gh_repo)
                        self.data.loc[len(self.data.index) + 1] = pd.Series(
                            {
                                "language": language,
                                "language_repo_bytes": bytes_count,
                                "repo_name": gh_repo.name,
                                "repo_owner_name": gh_repo.owner.login,
                                "repo_owner_url": gh_repo.owner.html_url,
                                "repo_url": gh_repo.html_url,
                                "repo_last_updated_date": gh_repo.updated_at,
                                "repo_description": gh_repo.description,
                            }
                        )

                if include_private or not gh_repo.private:  # respect privacy preference
                    repo = Repo(gh_repo)
                    self.repos[repo.status].append(repo)
        for status, repo_list in self.repos.items():
            repo_list.sort(reverse=True, key=lambda repo: repo.last_modified)
        last_updated_date = max(
            repo_list[0].last_modified for status, repo_list in self.repos.items()
        )
        with open("data/last_updated.txt", "w") as outfile:
            outfile.write(last_updated_date)

    def _get_gists(self, github, include_private=False):
        print("Collecting gists...")
        for gh_gist in github.get_user().get_gists():
            if include_private or gh_gist.public:
                gist = Gist(gh_gist)
                print(f"\t{gist.name}")
                self.gists.append(gist)
        self.gists.sort(reverse=True, key=lambda gist: gist.last_modified)

    @property
    def markdown_table(self):
        """
        :return: a list containing strings in markdown table format
        """
        table = [self.__class__.PROJECTS_HEADER]

        for status in self.repos:
            table.append(
                f"\n### {status}\n| Repository | Description | Owner | Language(s) |\n|---|---|---|---|\n"
            )
            for repo in self.repos[status]:
                table.append(repo.markdown)

        table.append(f"\n### Gists\n| Description |\n|---|\n")
        for gist in self.gists:
            table.append(gist.markdown)

        return table

    def write_markdown(
        self,
        out_filename="README.md",
        head_filename="config/head.md",
        tail_filename="config/tail.md",
    ):
        print(f"Updating the Projects table in {out_filename}...")
        with open(out_filename, "w") as out_file:
            with open(head_filename, "r") as head_file:
                out_file.writelines(head_file.readlines())
            out_file.writelines(self.markdown_table)
            with open(tail_filename, "r") as tail_file:
                out_file.writelines(tail_file.readlines())

    def write_csv(self, filename="data/repo_languages.csv"):
        self.data.to_csv(filename)

    def filter_owners(self, owner_names):
        self.data.query(f"repo_owner_name not in {owner_names}", inplace=True)


class Repo:
    """ Store info about a github repository """

    six_months = datetime.timedelta(days=182)

    def __init__(self, gh_repo):
        """ Store minimal info about a github repository
        :param gh_repo: a github repository object from pygithub
        """
        self.owner = f"[{gh_repo.owner.login}]({gh_repo.owner.html_url})"
        self.name = f"[{gh_repo.name}]({gh_repo.html_url})"
        self.description = gh_repo.description if gh_repo.description else ""
        self.languages = ", ".join(gh_repo.get_languages())
        self.language_bytes = gh_repo.get_languages()
        if gh_repo.archived:
            status = "Archive"
        elif (datetime.datetime.now() - gh_repo.updated_at) > self.__class__.six_months:
            status = "Stale"
        else:
            status = "Current"
        assert status in Projects.status_options
        self.status = status
        self.last_modified = gh_repo.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return (
            f"| {self.name} | {self.description} | {self.owner} | {self.languages} |\n"
        )

    @property
    def pd_series(self):
        return pd.Series(self.__dict__)


class Gist:
    def __init__(self, gh_gist):
        """ Store minimal info about a github Gist
        :param gh_gist: a github gist object from pygithub
        """
        self.name = gh_gist.description
        self.owner = f"[{gh_gist.owner.login}]({gh_gist.owner.html_url})"
        self.description = f"[{gh_gist.description}]({gh_gist.html_url})"
        self.last_modified = gh_gist.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.description} |\n"

    @property
    def pd_series(self):
        return pd.Series(self.__dict__)


def count_jupyter_bytes(gh_repo):
    """ Count bytes of code in Jupyter code blocks
    :param gh_repo: github repo from pygithub
    :return: bytes of code in code blocks
    """
    bytes_count = 0
    contents = gh_repo.get_contents("")
    while len(contents) > 1:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(gh_repo.get_contents(file_content.path))
        elif file_content.name.endswith(".ipynb"):
            if (
                file_content.size < 1e6
            ):  # TODO: need to use Git Data API to handle large Jupyter notebooks
                jsondict = json.loads(
                    base64.b64decode(file_content.content).decode("utf-8").strip("'")
                )
                for cell in jsondict["cells"]:
                    if cell["cell_type"] == "code":
                        for line in cell["source"]:
                            bytes_count += len(line.encode("utf-8"))
    return bytes_count


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)

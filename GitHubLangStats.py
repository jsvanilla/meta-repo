import base64
import collections
import datetime
import json
import pandas as pd
import plotly


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
            # print(file_content, file_content.type, file_content.size, file_content.name)
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


class Repos:
    """ Store information about a user's github repositories & generate a markdown table """

    status_options = ["Current", "Stale", "Archive"]

    PROJECTS_HEADER = "## Projects\n"

    def __init__(self, github, include_private=False):
        """
        :param github: a github object from pygithub
        :param include_private: whether to include private repositories
        """
        self.language_data = {
            "all_bytes": LangStat(
                "My languages by bytes of code on GitHub", "bytes of code", "all_bytes"
            ),
            "all_repos": LangStat(
                "My languages by presence in GitHub repositories",
                "# of repos",
                "all_repos",
            ),
            "top_bytes": LangStat(
                "Top repo languages by bytes of code on GitHub",
                "bytes of code",
                "top_bytes",
            ),
            "top_repos": LangStat(
                "Top languages by GitHub repositories", "# of repos", "top_repos"
            ),
        }
        self.repos = {status: [] for status in self.__class__.status_options}
        self._get_repos(github, include_private)
        self.gists = list()
        self._get_gists(github, include_private)
        self.plot_stats()

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
                )  # excludes vendored languages from the repo's .gitattributes
                for lang in (
                    "HTML",
                    "CSS",
                ):  # drop these because they're usually not hand-written by me
                    languages.pop(lang, None)
                if languages:
                    print(
                        f"\t\t\t{sorted(languages.keys(), key=lambda k: languages[k], reverse=True)}"
                    )
                    for (
                        lang,
                        bytes_count,
                    ) in languages.items():  # aggregate bytes counts for all languages
                        if lang == "Jupyter Notebook":
                            bytes_count = count_jupyter_bytes(gh_repo)
                        self.language_data["all_bytes"].add(lang, bytes_count)
                    self.language_data["all_repos"].update(languages.keys())
                    top_language = max(languages, key=lambda k: languages[k])
                    self.language_data["top_repos"].add(top_language, 1)
                    self.language_data["top_bytes"].add(
                        top_language,
                        count_jupyter_bytes(gh_repo)
                        if lang == "Jupyter Notebook"
                        else languages[top_language],
                    )
                # respect privacy preference
                if include_private or not gh_repo.private:
                    repo = Repo(gh_repo)
                    self.repos[repo.status].append(repo)

    def _get_gists(self, github, include_private=False):
        print("Collecting gists...")
        for gh_gist in github.get_user().get_gists():
            if include_private or gh_gist.public:
                gist = Gist(gh_gist)
                print(f"\t{gist.name}")
                self.gists.append(gist)
        self.gists.sort(reverse=True, key=lambda gist: gist.last_modified)

    def plot_stats(self):
        print("Making plots...")
        for stats in self.language_data.values():
            stats.make_plot()
            stats.make_plot(num_repos=7)
        for status, repo_list in self.repos.items():
            repo_list.sort(reverse=True, key=lambda repo: repo.last_modified)

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

    @property
    def pd_dataframe(self):
        df = pd.DataFrame(columns=Repo.__dict__.keys())
        for status in self.repos:
            for repo in self.repos[status]:
                df.loc[repo.name] = repo.pd_series
        return df

    def write_csv(self, filename):
        self.pd_dataframe.to_csv(filename)


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
        assert status in Repos.status_options
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
    def __init__(self, gist):
        """ Store minimal info about a github Gist
        :param gist: a github gist object from pygithub
        """
        self.name = gist.description
        self.owner = f"[{gist.owner.login}]({gist.owner.html_url})"
        self.description = f"[{gist.description}]({gist.html_url})"
        self.last_modified = gist.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.description} |\n"

    @property
    def pd_series(self):
        return pd.Series(self.__dict__)


class LangStat:
    def __init__(self, description, count_type, name):
        self.description = description
        self.count_type = count_type
        self.filename = f"figures/language_{name}"
        self.counter = collections.Counter()

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"

    def add(self, key, value):
        self.counter[key] += value

    def update(self, iterable):
        self.counter.update(iterable)

    def make_plot(self, num_repos=None):
        tuples = self.counter.most_common(num_repos)
        x = [lang[0] for lang in tuples]
        y = [lang[1] for lang in tuples]
        figure = plotly.graph_objs.Figure(
            data=[plotly.graph_objs.Bar(x=x, y=y, text=y, textposition="auto")],
            layout=plotly.graph_objs.Layout(
                title=self.description,
                xaxis=dict(tickangle=45),
                yaxis=dict(title=self.count_type, automargin=True),
            ),
        )
        plotly.io.write_image(
            figure,
            f"{self.filename}.svg"
            if not num_repos
            else f"{self.filename}_n{num_repos}.svg",
        )

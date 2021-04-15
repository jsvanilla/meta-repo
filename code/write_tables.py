import sys

sys.path.insert(
    0, "./"
)  # otherwise, snakemake looks in the conda env path and can't find GitHubLangStats

from code import GitHubLangStats

github = GitHubLangStats.login(token=snakemake.params.token)
projects = GitHubLangStats.Projects(
    github, include_private=snakemake.params.include_private
)
projects.write_csv(filename=snakemake.output.csv)

projects.filter_owners(snakemake.params.owners)
projects.write_markdown(
    out_filename=snakemake.output.md,
    head_filename=snakemake.input.head_md,
    tail_filename=snakemake.input.tail_md,
)

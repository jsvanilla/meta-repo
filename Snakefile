from code import GitHubLangStats

configfile: "config/config.yml"
github = GitHubLangStats.login(token_filename=config['token_filename'])
projects = GitHubLangStats.Projects(github, include_private=False)
#projects = GitHubLangStats.Projects.from_token(config['token_filename'])

rule targets:
    input:
        "README.md",
        "data/repo_languages.csv"

rule write_csv:
    output:
          csv="data/repo_languages.csv"
    run:
        projects.write_csv()

rule plot_language_stats:
    input:
         rules.write_csv.output.csv
    output:
          "figures/language_all_bytes.svg",
          "figures/language_all_bytes_n7.svg",
          "figures/language_all_repos.svg"
    script:
          "code/plot_language_stats.R"

rule write_markdown:
    input:
        head_md="config/head.md",
        tail_md="config/tail.md",
        figures=rules.plot_language_stats.output,
        csv=rules.write_csv.output.csv
    output:
        md="README.md"
    run:
        projects.write_markdown()


from code import GitHubLangStats

configfile: "config/config.yml"
github = GitHubLangStats.login(token_filename=config['token_filename'])

rule targets:
    input:
        "README.md",
        "data/repo_languages.csv"

rule write_csv:
    input:
        last_updated="data/last_updated.txt"
    output:
        csv="data/repo_languages.csv"
    run:
        projects = GitHubLangStats.Projects(github, include_private=False)
        projects.write_csv(filename=output.csv)

rule plot_language_stats:
    input:
         rules.write_csv.output.csv
    output:
          "figures/language_all_bytes.png",
          "figures/language_all_bytes_n7.png",
          "figures/language_all_repos.png"
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
        projects = GitHubLangStats.Projects(github, include_private=False)
        projects.filter_owners(config['ignore']['owners'])
        projects.write_markdown(out_filename=output.md, head_filename=input.head_md, tail_filename=input.tail_md)


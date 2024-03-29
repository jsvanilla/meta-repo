
## Usage

The [table above](#current) and [plots below](#plots) are generated by the snakemake workflow in the [`Snakefile`](Snakefile).

### Setup

1. Clone this repo:

    ```
    git clone https://github.com/kelly-sovacool/meta-repo
    ```

1. Change the URL to your own GitHub repo:

    ```
    git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
    ```

1. Install dependencies:

    ```
    conda env create -n git-repos -f config/environment.yaml
    conda activate git-repos
    ```

1. Generate an [access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) and paste it into a plain text file. Create a YAML file `config/config.yml` with the path to your token file:

    ```
    token_filename: path/to/token
    ```

    Don't share your token with anyone!

### Run it

Run the whole workflow with:

```
snakemake
```

It will collect information about repos you contribute to, write the data to
[csv](data/repo_languages.csv), update the README [`projects`](#projects) table,
& make [plots](##plots).

Don't edit the README file directly.
You can edit the [head](config/head.md) and [tail](config/tail.md) to modify
what appears before and after the projects table.

#### Alternate workflow

If you don't want to use snakemake, you can run the Python & R scripts in [`code/`](code).

```
python code/GitHubLangStats.py --token path_to_token
```

It will then collect the information from GitHub, write a csv file to [`data/`](data), 
and generate the table in [`README.md`](README.md) under the [`Projects`](#projects) subheading.
Only repositories which you own or which you have contributed to are included.

Alternatively, you can supply your username. It will then prompt you for your password:
```
python code/GitHubLangStats.py --username your_username
```

To update the plots, run the R script:
```
Rscript "code/plot_language_stats.R"
```

[Plots](##plots) of programming language statistics are written to [`figures/`](figures/).

#### Private repos

By default, private repos are excluded from the table.
However, they are always included in statistics for plots.
If you wish to include them, use the flag `--include_private`:

```
python code/GitHubLangStats.py --token path_to_token --include_private
```
or
```
python code/GitHubLangStats.py --username your_username --include_private
```

## Plots

![language_all_bytes](figures/language_all_bytes.png)

![langauge_all_bytes_n7](figures/language_all_bytes_n7.png)

![language_all_repos](figures/language_all_repos.png)

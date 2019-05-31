# meta-repo

A meta-repository to organize my public projects.

## Projects

### Current
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [hpc-config](https://github.com/kelly-sovacool/hpc-config) | Config files for Linux HPC accounts | [kelly-sovacool](https://github.com/kelly-sovacool) | Shell, Vim script |
| [meta-repo](https://github.com/kelly-sovacool/meta-repo) | A meta-repository to organize my public projects. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |
| [schlosslab.github.io](https://github.com/kelly-sovacool/schlosslab.github.io) | The website for the Schloss Lab at the University of Michigan | [kelly-sovacool](https://github.com/kelly-sovacool) | CSS, HTML, Ruby |
| [Great_Lakes_SLURM](https://github.com/SchlossLab/Great_Lakes_SLURM) | Using the Great Lakes cluster and batch computing with SLURM  | [SchlossLab](https://github.com/SchlossLab) |  |
| [PyCon_2019](https://github.com/GabrielleRab/PyCon_2019) | Repository for PyCon 2019 Education Summit Mini-Sprint: Workbooks that teach Python through scientific data exploration | [GabrielleRab](https://github.com/GabrielleRab) | Jupyter Notebook |
| [schlosslab.github.io](https://github.com/SchlossLab/schlosslab.github.io) | The website for the Schloss Lab at the University of Michigan | [SchlossLab](https://github.com/SchlossLab) | CSS, HTML, Ruby |
| [umswc.github.io](https://github.com/kelly-sovacool/umswc.github.io) | UM Software and Data Carpentry Website | [kelly-sovacool](https://github.com/kelly-sovacool) | CSS, HTML, Python, Ruby |
| [fitness-geek](https://github.com/kelly-sovacool/fitness-geek) | Having fun with my Strava data! | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |
| [kelly-sovacool.github.io](https://github.com/kelly-sovacool/kelly-sovacool.github.io) | My personal website, forked from the academicpages template. | [kelly-sovacool](https://github.com/kelly-sovacool) | Shell |
| [latex-cv](https://github.com/kelly-sovacool/latex-cv) | My curriculum vitae in LaTeX + a Snakemake pipeline for compiling tex to pdf. | [kelly-sovacool](https://github.com/kelly-sovacool) | TeX, Python, Shell |
| [documenting-R](https://github.com/SchlossLab/documenting-R) | Materials for a code review on documenting R code. | [SchlossLab](https://github.com/SchlossLab) | R |
| [SummerExperience](https://github.com/GWC-DCMB/SummerExperience) | materials for our Data Science Summer Experience  | [GWC-DCMB](https://github.com/GWC-DCMB) | Jupyter Notebook |
| [lang-stats](https://github.com/kelly-sovacool/lang-stats) | Collect & plot personal programming language statistics from GitHub repos | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |
| [snakemake_hpc_mwe](https://github.com/kelly-sovacool/snakemake_hpc_mwe) | A minimal working example of using Snakemake on the HPC | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, Shell |
| [CapstoneProject](https://github.com/GWC-DCMB/CapstoneProject) | Capstone Project Information for 2017-2018 GWC | [GWC-DCMB](https://github.com/GWC-DCMB) | Jupyter Notebook, HTML, Python |
| [advent-of-code-2018](https://github.com/kelly-sovacool/advent-of-code-2018) | My solutions to the Advent of Code 2018 puzzles. | [kelly-sovacool](https://github.com/kelly-sovacool) | Jupyter Notebook, Python, Shell |
| [tiger_salamander_project](https://github.com/kelly-sovacool/tiger_salamander_project) | SNP pipeline using Snakemake for the Weisrock Lab's Tiger Salamander project. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, Shell |
| [codeDemos](https://github.com/GWC-DCMB/codeDemos) | Coding demos for Python instruction in Girls Who Code Club | [GWC-DCMB](https://github.com/GWC-DCMB) | Jupyter Notebook, Python |
| [stats-ref](https://github.com/kelly-sovacool/stats-ref) | A reference for concepts & equations in statistics. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, CSS |

### Stale
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [tcf-words](https://github.com/c-andy-martin/tcf-words) | TCF Overhead Words | [c-andy-martin](https://github.com/c-andy-martin) |  |
| [useful-programs](https://github.com/thesuperlab/useful-programs) | None | [thesuperlab](https://github.com/thesuperlab) | Python, Shell |

### Archive
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [miRNA-diff-expr](https://github.com/kelly-sovacool/miRNA-diff-expr) | Differential expression analysis for miRNA sequence data | [kelly-sovacool](https://github.com/kelly-sovacool) | R |
| [undergrad-comp-sci](https://github.com/kelly-sovacool/undergrad-comp-sci) | A collection of code I wrote for assignments in computer science courses as an undergraduate student at the University of Kentucky (2014-2018). | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, C++, Ruby, PHP, JavaScript, Perl, R, HTML, CSS, Makefile, CoffeeScript |
| [dmrr-submission-prep](https://github.com/kelly-sovacool/dmrr-submission-prep) | Prepare miRNA metadata for submission to the exRNA Data Coordination Center | [kelly-sovacool](https://github.com/kelly-sovacool) | Jupyter Notebook, Python |
| [geo109-project](https://github.com/kelly-sovacool/geo109-project) | Lexington collision maps for GEO109 | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |

## Usage

The table above is generated by the script [`git-repos.py`](git-repos.py). If you wish to use it to generate your own table of repos, follow these instructions:

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
    conda env create -n git-repos -f environment.yaml
    conda activate git-repos
    ```

1. Update the README file with a table of your projects with:

    ```
    python git-repos.py --username your_username
    ```
    It will then prompt you for your GitHub password, collect the information from GitHub, and generate the table in [`README.md`](README.md) under the [`Projects`](#projects) subheading. It will only include repositories which you own or which you have contributed to.

    By default it will exclude private repos from the table.
    If you wish to include them, use the flag `--include_private`:
    ```
    python git-repos.py --username your_username --include_private
    ```

## TO-DO
- Merge the functionality of [lang-stats](https://api.github.com/repos/kelly-sovacool/lang-stats) into this project.
- Option to use API token instead of GitHub username & password.

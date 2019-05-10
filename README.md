# meta-repo

A meta-repository to organize my public projects.

## Projects

### Current
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [lang-stats](https://api.github.com/repos/kelly-sovacool/lang-stats) | Collect & plot personal programming language statistics from GitHub repos | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |
| [meta-repo](https://api.github.com/repos/kelly-sovacool/meta-repo) | A meta-repository to organize my public projects. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |
| [snakemake_hpc_mwe](https://api.github.com/repos/kelly-sovacool/snakemake_hpc_mwe) | A minimal working example of using Snakemake on the HPC | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, Shell |
| [PyCon_2019](https://api.github.com/repos/GabrielleRab/PyCon_2019) | Repository for PyCon 2019 Education Summit Mini-Sprint: Workbooks that teach Python through scientific data exploration | [GabrielleRab](https://github.com/GabrielleRab) | Jupyter Notebook |
| [CapstoneProject](https://api.github.com/repos/GWC-DCMB/CapstoneProject) | Capstone Project Information for 2017-2018 GWC | [GWC-DCMB](https://github.com/GWC-DCMB) | Jupyter Notebook, HTML, Python |
| [advent-of-code-2018](https://api.github.com/repos/kelly-sovacool/advent-of-code-2018) | My solutions to the Advent of Code 2018 puzzles. | [kelly-sovacool](https://github.com/kelly-sovacool) | Jupyter Notebook, Python, Shell |
| [kelly-sovacool.github.io](https://api.github.com/repos/kelly-sovacool/kelly-sovacool.github.io) | My personal website, forked from the academicpages template. | [kelly-sovacool](https://github.com/kelly-sovacool) | Shell |
| [latex-cv](https://api.github.com/repos/kelly-sovacool/latex-cv) | My curriculum vitae in LaTeX + a Snakemake pipeline for compiling tex to pdf. | [kelly-sovacool](https://github.com/kelly-sovacool) | TeX, Python |
| [schlosslab.github.io](https://api.github.com/repos/SchlossLab/schlosslab.github.io) | The website for the Schloss Lab at the University of Michigan | [SchlossLab](https://github.com/SchlossLab) | CSS, HTML, Ruby |
| [tiger_salamander_project](https://api.github.com/repos/kelly-sovacool/tiger_salamander_project) | SNP pipeline using Snakemake for the Weisrock Lab's Tiger Salamander project. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, Shell |
| [codeDemos](https://api.github.com/repos/GWC-DCMB/codeDemos) | Coding demos for Python instruction in Girls Who Code Club | [GWC-DCMB](https://github.com/GWC-DCMB) | Jupyter Notebook, Python |
| [stats-ref](https://api.github.com/repos/kelly-sovacool/stats-ref) | A reference for concepts & equations in statistics. | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, CSS |

### Stale
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [tcf-words](https://api.github.com/repos/c-andy-martin/tcf-words) | TCF Overhead Words | [c-andy-martin](https://github.com/c-andy-martin) |  |
| [useful-programs](https://api.github.com/repos/thesuperlab/useful-programs) | None | [thesuperlab](https://github.com/thesuperlab) | Python, Shell |

### Archive
| Repository | Description | Owner | Language(s) |
|---|---|---|---|
| [miRNA-diff-expr](https://api.github.com/repos/kelly-sovacool/miRNA-diff-expr) | Differential expression analysis for miRNA sequence data | [kelly-sovacool](https://github.com/kelly-sovacool) | R |
| [undergrad-comp-sci](https://api.github.com/repos/kelly-sovacool/undergrad-comp-sci) | A collection of code I wrote for assignments in computer science courses as an undergraduate student at the University of Kentucky (2014-2018). | [kelly-sovacool](https://github.com/kelly-sovacool) | Python, C++, Ruby, PHP, JavaScript, Perl, R, HTML, CSS, Makefile, CoffeeScript |
| [dmrr-submission-prep](https://api.github.com/repos/kelly-sovacool/dmrr-submission-prep) | Prepare miRNA metadata for submission to the exRNA Data Coordination Center | [kelly-sovacool](https://github.com/kelly-sovacool) | Jupyter Notebook, Python |
| [geo109-project](https://api.github.com/repos/kelly-sovacool/geo109-project) | Lexington collision maps for GEO109 | [kelly-sovacool](https://github.com/kelly-sovacool) | Python |

## Usage

The table above is generated by the script [`git-repos.py`](git-repos.py). If you wish to use it to generate your own table of repos, follow these instructions:

1. Clone this repo.

    ```
    git clone https://github.com/kelly-sovacool/meta-repo
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
    It will then prompt you for your GitHub username & password, collect the information from github, and generate the table in `README.md`. It will only include repositories which you own or which you have contributed to.

    By default it will exclude private repos from the table.
    If you wish to include them, use the flag `--include_private`:
    ```
    python git-repos.py --username your_username --include_private
    ```
## TO-DO
- Merge the functionality of [lang-stats](https://api.github.com/repos/kelly-sovacool/lang-stats) into this project.

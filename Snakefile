from datetime import datetime
from pathlib import Path

configfile: "config/config.yml"

if 'token' in config and config['token']:
    token = config['token']
elif config['token_filename']:
    with open(config['token_filename'], 'r') as file:
        token = file.readline().strip()
else:
    raise ValueError("No token provided for GitHub access")

date_filename = 'data/last_updated.txt'
with open(date_filename, 'r') as file:
    now = datetime.now()
    last_updated = datetime.strptime(file.readline().strip(), '%Y-%m-%d')
    delta_days = (now - last_updated).days
    if delta_days > 0:
        Path(date_filename).touch()


rule targets:
    input:
        "README.md",
        "figures/language_all_bytes_n7.png"

rule write_tables:
    input:
        last_updated=date_filename,
        code='code/write_tables.py',
        head_md="config/head.md",
        tail_md="config/tail.md",
    output:
        csv="data/repo_languages.csv",
        md="README.md"
    params:
        token=token,
        include_private=config['include_private'],
        owners=config['ignore']['owners']
    script:
        "code/write_tables.py"

rule plot_language_stats:
    input:
         rules.write_tables.output.csv
    output:
          "figures/language_all_bytes.png",
          "figures/language_all_bytes_n7.png",
          "figures/language_all_repos.png"
    script:
          "code/plot_language_stats.R"

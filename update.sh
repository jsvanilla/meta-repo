#!/bin/bash
source ~/.bash_profile
conda activate git-repos
python git-repos.py -t .token
git add .
git commit -m "Auto-update repos"
git push

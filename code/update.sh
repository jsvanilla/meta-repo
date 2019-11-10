#!/bin/bash

function update() {
    source ~/.bash_profile
    conda activate git-repos
    snakemake
}

function commit() {
    git add README.md figures/
    git commit -m "Auto-update repos"
    git push
}

if update; then
    commit
else
    echo "* Update failed! *"
fi

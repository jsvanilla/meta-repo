#!/bin/bash

function update() {
    source ~/.bash_profile
    conda activate git-repos
    snakemake
}

function commit() {
    git add .
    git commit -m "Auto-update repos" || echo "No changes to commit"
    git push || echo "No changes to push"
}

if update; then
    commit
else
    echo "* Update failed! *"
fi

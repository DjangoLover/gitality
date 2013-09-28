#!/bin/bash

project_name=gitality
virtualenv_path=$WORKON_HOME/$project_name

source `which virtualenvwrapper.sh`

# Delete existent virutal environment
if [[ -d $virtualenv_path ]]; then
    rmvirtualenv $project_name > /dev/null
fi

# Create fresh virtual environment
mkvirtualenv -q $project_name > /dev/null 2>&1

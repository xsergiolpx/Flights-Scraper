#!/usr/bin/env bash

# Project name

project="not-null"
project=$1

# Project with time and date
t=$(date +"%d-%m-%Y-%Hh-%Mm-%Ss")

mv $project $project-$t
mv $project-$t old

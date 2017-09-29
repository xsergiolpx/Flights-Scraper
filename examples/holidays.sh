#!/usr/bin/env bash

# Project name
project="projects/holidays"

# Your email
email=“YOUR_EMAIL”

# Subject of the email
subject="Flights to South Africa or Cuba"

# Where to save the links
links=$project"/links/links.txt"

# Where to save the results
folder_results=$project"/csv/"

# Example
./clean-project.sh $project

# Create the dirs

mkdir -p $project"/csv"
mkdir -p $project"/links"
mkdir -p $project"/html"
mkdir -p $project"/javascripts"

python generate_links_kayak.py -a 02 -b 02 -y 2018 -z 2018 -d ROM -r CPT -e es -n $links
python generate_links_kayak.py -a 02 -b 02 -y 2018 -z 2018 -d MAD -r CPT -e es -n $links
python generate_links_kayak.py -a 02 -b 02 -y 2018 -z 2018 -d ROM -r VRA -e es -n $links
python generate_links_kayak.py -a 02 -b 02 -y 2018 -z 2018 -d MAD -r HAV -e es -n $links

python main.py $project phantomjs 180
python analyze.py $folder_results

cat $project/csv/results.html | mail -s "$(echo -e $subject '\nContent-Type: text/html\nMime-Version: 1.0')" $email

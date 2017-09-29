#!/usr/bin/env bash

# Project name
project="projects/weekend"

# Your email
email=“YOUR_EMAIL”

# Subject of the email
subject="Flights Rome to Madrid"

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

python generate_links_kayak_short_trip.py -a 10 -b friday -y 2017 -z monday -d ROM -r MAD -e es -n $links
python generate_links_kayak_short_trip.py -a 11 -b friday -y 2017 -z monday -d ROM -r MAD -e es -n $links
python generate_links_kayak_short_trip.py -a 12 -b friday -y 2017 -z monday -d ROM -r MAD -e es -n $links

python main.py $project phantomjs 30
python analyze.py $folder_results

cat $project/csv/results.html | mail -s "$(echo -e $subject '\nContent-Type: text/html\nMime-Version: 1.0')" $email

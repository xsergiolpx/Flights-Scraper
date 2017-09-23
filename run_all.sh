#!/usr/bin/env bash

# Example
./clean.sh
python generate_links_kayak.py -a 10 -b 00 -y 2017 -z 2017 -d ROM -r AMS -e es -n links/links.txt
python generate_links_kayak.py -a 11 -b 00 -y 2017 -z 2017 -d ROM -r AMS -e es -n links/links.txt
python generate_links_kayak.py -a 12 -b 00 -y 2017 -z 2017 -d ROM -r AMS -e es -n links/links.txt
python generate_links_kayak.py -a 10 -b 00 -y 2017 -z 2017 -r ROM -d AMS -e es -n links/links.txt
python generate_links_kayak.py -a 11 -b 00 -y 2017 -z 2017 -r ROM -d AMS -e es -n links/links.txt
python generate_links_kayak.py -a 12 -b 00 -y 2017 -z 2017 -r ROM -d AMS -e es -n links/links.txt
python generate_links_kayak.py -a 10 -b 00 -y 2017 -z 2017 -d ROM -r MAD -e es -n links/links.txt
python generate_links_kayak.py -a 11 -b 00 -y 2017 -z 2017 -d ROM -r MAD -e es -n links/links.txt
python generate_links_kayak.py -a 12 -b 00 -y 2017 -z 2017 -d ROM -r MAD -e es -n links/links.txt
python generate_links_kayak.py -a 10 -b 00 -y 2017 -z 2017 -r ROM -d MAD -e es -n links/links.txt
python generate_links_kayak.py -a 11 -b 00 -y 2017 -z 2017 -r ROM -d MAD -e es -n links/links.txt
python generate_links_kayak.py -a 12 -b 00 -y 2017 -z 2017 -r ROM -d MAD -e es -n links/links.txt
python main.py links/links.txt phantomjs 60
python analyze.py csv/

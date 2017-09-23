#!/usr/bin/env bash

# Example
./clean.sh
python generate_links_kayak.py -a 05 -b 06 -y 2018 -z 2018 -d MAD,BCN -r BKK,KUL -e es -n links/links.txt
python main.py links/links.txt phantomjs
python analyze.py csv/
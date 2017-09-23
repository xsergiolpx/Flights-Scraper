#!/usr/bin/env bash

./clean.sh
python generate_links_kayak.py -a 01 -b 01 -y 2018 -z 2018 -d ROM -r MAD -e es -n links/links.txt
python main.py
python analyze.py

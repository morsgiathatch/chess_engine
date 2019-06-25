#!/usr/bin/env bash
# this script generates all data useful to the machine-learning aspect of the project
cd ./Scraper/
bash ./scrape.sh
cd ../Parser/
python3 Parser.py
python3 vectorize_games.py

#!/usr/bin/env bash
# this script generates all data useful to the machine-learning aspect of the project
python3 ./Scraper/Scrape.py
cd ./Scraper/zips/
unzip '*.zip'
rm -rf '*.zip'
for t in *.pgn
do
    mv ${t} ../../Parser/games
done
cd ../../
pwd
cd ./Parser/
python3 Parser.py
cd ../Board
python3 vectorize_games.py
cd ../

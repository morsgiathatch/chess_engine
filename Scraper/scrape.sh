#!/usr/bin/env bash

python3 Scrape.py
cd ./zips/
unzip '*.zip'
rm -rf '*.zip'
for t in *.pgn
do
    mv ${t} ../Parser/games
done
cd ../
#!/bin/bash

## This script uses https://github.com/cahya-wirawan/artificial-commonvoice to
## generates synthetic voices. It reads the SOURCE_FILE to retrieve the sound file name and its sentences.
## It generates 4 voice types for each sentence: id-ID-Wavenet-A, id-ID-Wavenet-B, id-ID-Wavenet-C, id-ID-Wavenet-D.
## It starts from the line number START+1 to the line number END of SOURCE_FILE.
## The result will be stored in DESTINATION_DIR.

## Please update following SOURCE_FILE and DESTINATION_DIR accordingly
SOURCE_FILE="/mnt/mldata/data/ASR/news/id-newspapers-small.tsv"
DESTINATION_DIR="/mnt/mldata/data/ASR/news/id-newspapers"

## Please uncomment the variable START according to your name

## Cahya
#START=0

## Galuh
#START=100000

## Akmal
#START=200000

## Yasir
#START=300000

# Agung
#START=400000

## Samsul
#START=500000

# Length is *ten thousand* lines. Since we use 4 voice types, it will generate 4*10000 synthetic sound files.
LENGTH=10000
END=$((START+LENGTH))

if [ -z ${START} ]
then
  echo "Please set the env variable START properly"
else
  python commonvoice.py --debug -s -t 0.15 -c "${SOURCE_FILE}" -v id-ID-Wavenet-A id-ID-Wavenet-B id-ID-Wavenet-C id-ID-Wavenet-D --start "${START}" --end "${END}" -o "${DESTINATION_DIR}"
fi
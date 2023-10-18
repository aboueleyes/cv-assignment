#!/bin/bash

URLS=$(cat urls.txt)

# name them 1.jpg, 2.jpg, 3.jpg, etc.
i=1
for URL in $URLS; do
    wget -O images/original/$i.jpg $URL
    i=$((i+1))
done
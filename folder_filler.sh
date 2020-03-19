#!/bin/bash

workin_dir=$1
cd $workin_dir
file_extentions=(txt mp3 pdf psd mp4 jpg png zip exe css)
times=(202003150000 202003080000 202003010000 202002250000 202002180000)
for ext in "${file_extentions[@]}"; do
    for time in "${times[@]}"; do
        touch -mt "$time" "$time.$ext"
    done;
done;


#!/bin/bash

workin_dir=$1
cd $workin_dir
file_extentions=(txt mp3 pdf psd mp4 jpg png zip exe css)
times=( 201909150000 201910150000 202001150000 202002150000 202002160000 202002180000 202002190000 202002200000 202002210000 202002080000 202002010000 202001250000 202001180000 202003180000)
for ext in "${file_extentions[@]}"; do
    for time in "${times[@]}"; do
        touch -mt "$time" "$time.$ext"
    done;
done;


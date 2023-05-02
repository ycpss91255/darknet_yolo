#!/usr/bin/env bash

# adjustable parameters
train_ratio=90

# do not tune parameters unless necessary
train_file="train.txt"
valid_file="valid.txt"
obj_folder="$(readlink -f obj)"
# Non-tunable parameters
jpg_list=()

# get object list
jpg_list=("${obj_folder}"/*.jpg)

jpg_num=${#jpg_list[@]}
train_num=$(echo "scale=0; ${jpg_num} * ${train_ratio} / 100" | bc)

# write train object list to train file
printf "%s\n" "${jpg_list[@]:0:${train_num}}" >${train_file}

printf "%s\n" "${jpg_list[@]:$((train_num + 1))}" >${valid_file}

# print paramters
echo -e "obj_folder: ${obj_folder}
train_file: ${train_file}
valid_file: ${valid_file}
-----------
train_ratio: ${train_ratio}%
valid_ratio: $((100 - train_ratio))%
total object num: ${jpg_num}
train_num: ${train_num}
valid_num: $((jpg_num - train_num))" | column -t -s ':'

#!/usr/bin/env bash

# $1 - path to save dir

save_dir="${1:-"$(dirname "$(readlink -f "${0}")")"}"

if [[ -z $(find "${save_dir}/server_data" -mindepth 1 -print -quit 2>/dev/null) ]]; then
    echo "file not found: ${save_dir}/server_data"
else
    sudo rm -rf "${save_dir}/server_data" > /dev/null 2>&1 && \
    echo -e "remove dircetory file : ${save_dir}/server_data\ndone"
fi

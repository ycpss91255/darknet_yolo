#!/usr/bin/env bash

# $1 - path to save dir

save_dir="${1:-"$(dirname "$(readlink -f "${0}")")"}"

echo "Save dir: ${save_dir}"
if [[ -z $(find "${save_dir}/server_data" -mindepth 1 -print -quit 2>&1) ]]; then
    mkdir -p "${save_dir}"/server_data
fi

chmod 0777 "${save_dir}/server_data" && \
docker run \
    -it \
    -p 8080:8080 \
    -v "${save_dir}"/server_data:/label-studio/data \
    heartexlabs/label-studio:latest

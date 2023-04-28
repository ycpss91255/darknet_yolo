#!/usr/bin/env bash

# $1 - path to save dir

save_dir="${1:-"$(dirname "$(readlink -f "${0}")")"}"

if [[ ! -d "${save_dir}/server_data" ]]; then
    mkdir -p "${save_dir}"/server_data
    echo "Created dir: ${save_dir}/server_data"
fi

echo "Save dir: ${save_dir}"

chmod 0777 "${save_dir}/server_data" && \
docker run \
    -it \
    --rm \
    -p 8080:8080 \
    -v "${save_dir}"/server_data:/label-studio/data \
    heartexlabs/label-studio:latest

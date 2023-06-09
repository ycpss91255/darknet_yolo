FROM nvidia/cuda:12.0.1-cudnn8-devel-ubuntu22.04
############################## SYSTEM PARAMETERS ##############################
# * Arguments
ARG USER=initial
ARG GROUP=initial
ARG UID=1000
ARG GID="${UID}"
ARG SHELL=/bin/bash
ARG HARDWARE=x86_64
ARG ENTRYPOINT_FILE=entrypint.sh

# * Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all
# ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

# * Setup users and groups
RUN groupadd --gid "${GID}" "${GROUP}" && \
    useradd --gid "${GID}" --uid "${UID}" -ms "${SHELL}" "${USER}" && \
    mkdir -p /etc/sudoers.d && \
    echo "${USER}:x:${UID}:${UID}:${USER},,,:/home/${USER}:${shell}" >> /etc/passwd && \
    echo "${USER}:x:${UID}:" >> /etc/group && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
    chmod 0440 "/etc/sudoers.d/${USER}"

# * Replace apt urls
# ? Change to tku
RUN sed -i 's@archive.ubuntu.com@ftp.tku.edu.tw@g' /etc/apt/sources.list
# ? Change to Taiwan
# RUN sed -i 's@archive.ubuntu.com@tw.archive.ubuntu.com@g' /etc/apt/sources.list

# * Time zone
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/"${TZ}" /etc/localtime && echo "${TZ}" > /etc/timezone

############################### INSTALL #######################################
# * Install packages
RUN apt update && \
    apt install -y --no-install-recommends \
        sudo \
        git \
        htop \
        wget \
        curl \
        psmisc \
        # * Shell
        tmux \
        terminator \
        # * base tools
        vim \
        python3-pip \
        python3-dev \
        python3-setuptools \
        # darknet
        pkg-config \
        build-essential \
        libopencv-dev \
        # pytorch-YOLOv4
        # libfreetype6-dev \
        # * Work tools
    && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# * check your GPU Compute Capability
# use `nvidia-smi -L` look your GPU name, and check your GPU Compute Capability
# Reference: https://developer.nvidia.com/cuda-gpus
# GeForce GTX 1080 Ti
ARG CUDA_ARCH_BIN=61
# GeForce GTX 2080 Ti
# ARG CUDA_ARCH_BIN=75
# GeForce GTX 3090
# ARG CUDA_ARCH_BIN=86

# * Install darknet
RUN git clone https://github.com/AlexeyAB/darknet.git /home/"${USER}"/darknet && \
    sed -i 's/GPU=0/GPU=1/g' /home/"${USER}"/darknet/Makefile && \
    sed -i 's/CUDNN=0/CUDNN=1/g' /home/"${USER}"/darknet/Makefile && \
    sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/g' /home/"${USER}"/darknet/Makefile && \
    sed -i 's/OPENCV=0/OPENCV=1/g' /home/"${USER}"/darknet/Makefile && \
    sed -i 's/ARCH= -gencode arch=compute_35,code=sm_35/ARCH= -gencode arch=compute_${CUDA_ARCH_BIN},code=sm_${CUDA_ARCH_BIN}/g' /home/"${USER}"/darknet/Makefile && \
    make -C /home/"${USER}"/darknet && \
    chown -R "${USER}":"${GROUP}" /home/"${USER}"/darknet

ENV PATH="/home/"${USER}"/darknet:${PATH}"

############################### OTHER #######################################
# * Copy entrypoint
# ? Requires docker version >= 17.09
COPY --chmod=0775 ./${ENTRYPOINT_FILE} /entrypoint.sh
# ? docker version < 17.09
# COPY ./${ENTRYPOINT_FILE} /entrypoint.sh
# RUN sudo chmod 0775 /entrypoint.sh

# * Copy custom configuration
# ? Requires docker version >= 17.09
COPY --chown="${USER}":"${GROUP}" --chmod=0775 config config
# ? docker version < 17.09
# COPY config config
# RUN sudo chown -R "${USER}":"${GROUP}" config \
    # && sudo chmod -R 0775 config

# * Install python packages
RUN ./config/pip/pip_setup.sh

############################## USER CONFIG ####################################
# * Switch user to ${USER}
USER ${USER}

# * Setup user configuration
RUN ./config/shell/bash_setup.sh "${USER}" "${GROUP}" && \
    ./config/shell/terminator/terminator_setup.sh "${USER}" "${GROUP}" && \
    ./config/shell/tmux/tmux_setup.sh "${USER}" "${GROUP}" && \
    sudo rm -rf /config

# * Switch workspace to /home/"${USER}"/work
RUN sudo mkdir /home/"${USER}"/work
WORKDIR /home/"${USER}"/work

# ENTRYPOINT [ "/entrypoint.sh", "terminator" ]
# ENTRYPOINT [ "/entrypoint.sh", "tmux" ]
ENTRYPOINT [ "/entrypoint.sh", "bash" ]
# ENTRYPOINT [ "/entrypoint.sh" ]

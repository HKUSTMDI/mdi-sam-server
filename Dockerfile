FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

RUN apt-get update \
    && apt-get install --no-install-recommends -y iputils-ping net-tools curl vim wget gcc make openssh-client libssl-dev

ENV TIME_ZONE=Asia/Shanghai
RUN echo "${TIME_ZONE}" > /etc/timezone && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=/opt/miniconda/bin:$PATH
    
ENV CONDA_DIR /opt/miniconda
RUN curl -sLo ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && chmod +x ~/miniconda.sh \
    && ~/miniconda.sh -b -p /opt/miniconda \
    && rm ~/miniconda.sh

ENV PATH=$CONDA_DIR/bin:$PATH

WORKDIR /app
COPY . .
# Installing python dependesncies
RUN python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && python3 -m pip --no-cache-dir install --upgrade pip \
    && apt-get install git -y

RUN pip install -e .

VOLUME ["/app/models"]

ENV SERVER_PORT=9091

EXPOSE ${SERVER_PORT}

CMD ["/bin/bash","./bin/start.sh"]
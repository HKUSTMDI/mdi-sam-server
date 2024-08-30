#!/bin/bash
shell_path=`cd $(dirname $0);pwd`
dir_path=`dirname $shell_path`


cd  $dir_path
source ./.env
APP="./src/mdi_sam_server"
cd $APP

SAM_CHOICE=SAM2
SAM2_CHECKPOINT=./models/sam2_hiera_base_plus.pt
SAM2_CONFIG=sam2_hiera_b+.yaml

log_level=INFO

mdi_sam_server run --port $SERVER_PORT --log-level $log_level
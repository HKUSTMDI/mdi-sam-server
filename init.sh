#!/bin/bash
path=`dirname $0`

# copy .env file
cd $path
cp .env_example .env

# download models
cd models
/bin/bash download_ckpts.sh

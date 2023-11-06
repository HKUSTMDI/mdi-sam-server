#!/bin/bash

# Execute the gunicorn command
#gunicorn --preload --bind :9091 --workers 1 --threads 8 --timeout 0 _wsgi:app
#nohup python3 _wsgi.py --port 9091 >> run.log &

SHELL_DIR=$(cd $(dirname $0);pwd)
BASE_DIR=$(cd $(dirname $0);cd ..;pwd)
LOG_DIR=${BASE_DIR}/log
PID_FILE=${LOG_DIR}/PID

SERVER_MAIN="${SHELL_DIR}/_wsgi.py"
CMD_LINE="python3 ${SERVER_MAIN} --port 9090"


start() {
    if [ ! -f "${SERVER_MAIN}" ];then
        echo `date +"%F %T"` - ERROR - Can not find ${SERVER_MAIN} ...
        exit 1
    fi

    PID=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|awk '{print $1}'`
    if [ x"${PID}" == x"" ];then
        cd ${SHELL_DIR}
        mkdir -p ${LOG_DIR}
        nohup ${CMD_LINE} >> ${LOG_DIR}/server.log 2>&1 &
        # place the following shell sentence right after the nohup statement
        PID=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|awk '{print $1}'`
        echo "`date +"%F %T"` - start ${SERVER_MAIN} "
    else
        echo "`date +"%F %T"` - ERROR - PID:${PID} exist. ${SERVER_MAIN} is already running."
    fi
    echo ${PID} > ${PID_FILE}
}

stop() {
    PID=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|awk '{print $1}'`
    if [ x"${PID}" == x"" ];then
        echo "`date +"%F %T"` - ERROR - ${SERVER_MAIN} is not running..."
    else
        kill -15 $PID
        while true
        do
            if test $( ps aux | awk '{print $2}' | grep -w "$PID" | grep -v 'grep' | wc -l ) -eq 0;then
                echo "`date +"%F %T"` - SUCCESS - ${SERVER_MAIN} has been stopped..."
                break
            else
                echo "`date +"%F %T"` - wait to stop..."
                sleep 1
            fi
        done
    fi
}

kill9() {
    PID=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|awk '{print $1}'`
    if [ x"${PID}" == x"" ];then
        echo "`date +"%F %T"` - ERROR - ${SERVER_MAIN} is not running..."
        exit 1
    else
        kill -9 $PID
    fi
}

restart() {
    stop
    start
}

monitor() {
    check_num=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|wc -l`
    if [ $check_num -eq 0 ];then
        start
        echo `date +"%F %T"` - restart.
    else
        PID=`ps ax -o pid,cmd|grep "$CMD_LINE"|grep -v grep|awk '{print $1}'`
        echo ${PID} > ${PID_FILE}
    fi
}

case "$1" in
    "start")
      start;
    ;;
    "stop")
      stop;
    ;;
    "restart")
      restart;
    ;;
    "kill9")
      kill9;
    ;;
    "monitor")
      monitor;
    ;;
  *)
    echo "Usage: $(basename "$0") start/stop/restart/kill9/monitor"
    exit 1
esac

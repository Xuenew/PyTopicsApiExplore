#!/bin/bash
cd /home/temp/PyTopicsApiExplore
g_stash_str=`git stash`
g_pull_str=`git pull`
yy=`echo "$g_stash_str"`
xx=`echo "$g_pull_str"`
alre="Already up to date"
begain_time=`date`
if [[ $g_pull_str =~ "Already up to date" ]]
then
    echo "git 正常不需要热更新！！！$begain_time"
else
    /home/temp/env_pytopicsapiexplore/bin/uwsgi --reload /home/temp/uwsgi.pid
    echo "已经完成热更新！！$begain_time"
fi

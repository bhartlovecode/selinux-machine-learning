#!/bin/bash

dir=/home/mlserver/selinux-machine-learning/containers/
port=$1

apptainer instance start \
--pid-file /run/ml-containers/$port/pid \
--net --network-args "portmap=$port:8000/tcp" \
$dir/ml-container.sif ml-container-$port

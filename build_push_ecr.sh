#!/usr/bin/env bash

set -e

ECR="598490276344.dkr.ecr.us-east-1.amazonaws.com/sudoku-solver"

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 598490276344.dkr.ecr.us-east-1.amazonaws.com
docker build -t ${ECR}:latest .
docker push ${ECR} --all-tags


# Run docker locally

# docker run -i -t -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw gui
# "sudo xhost",
# "sudo xhost +local:docker",
# "sudo docker run -i -t -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw 598490276344.dkr.ecr.us-east-1.amazonaws.com/sudoku-solver:latest"
# ssh -L 5901:localhost:5901 ec2-user@ec2-50-19-199-203.compute-1.amazonaws.com

#!/bin/sh

rm -rf InStock
rsync -av --progress ../../InStock . --exclude .git --exclude .idea --exclude *.md --exclude *.bat --exclude __pycache__ --exclude .gitignore --exclude InStock/cron --exclude InStock/img --exclude InStock/docker --exclude instock/cache --exclude instock/log --exclude instock/test
rm -rf cron
cp -r ../../InStock/cron .

DOCKER_NAME=mayanghua/instock
TAG1=$(date "+%Y%m")
TAG2=latest

echo " docker build -f Dockerfile -t ${DOCKER_NAME} ."
docker build -f Dockerfile -t ${DOCKER_NAME}:${TAG1} -t ${DOCKER_NAME}:${TAG2} .
echo "#################################################################"
echo " docker push ${DOCKER_NAME} "

docker push ${DOCKER_NAME}:${TAG1}
docker push ${DOCKER_NAME}:${TAG2}
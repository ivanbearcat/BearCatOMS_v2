#!/bin/bash
cd /usr/share/nginx/BearCatOMS_v2/gitlab_hook
git pull
tsc
docker build --rm -f "Dockerfile" -t registry.cn-shanghai.aliyuncs.com/xiaohulu/viproom-micro-service:web_hook . && docker push registry.cn-shanghai.aliyuncs.com/xiaohulu/viproom-micro-service

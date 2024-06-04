#!/bin/bash
docker build --platform linux/amd64 -t hub.klr.kr/gq . && \
docker push hub.klr.kr/gq
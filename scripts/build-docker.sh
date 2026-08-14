#!/bin/bash

set -e

docker build -t registry.sweetrpg.com/sweetrpg-shared-web:latest .
docker push registry.sweetrpg.com/sweetrpg-shared-web

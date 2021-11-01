#!/bin/bash

set -e

ns=${1:-sweetrpg-support}

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

pushd ${scriptdir}

echo "Deleting old secrets..."
kubectl delete -n "${ns}" secret sweetrpg-registry shared-web-files shared-web-cache shared-web-auth shared-web-misc shared-web-common || true

echo "Docker registry config..."
kubectl create -n "${ns}" secret docker-registry sweetrpg-registry \
    --docker-server=registry.sweetrpg.com \
    --docker-username=docker \
    --docker-password=ESU7PnNtlt07zkvbnSyByrTdzllajxIQWqY7mswQR78
#kubectl create -n "${ns}" secret dockerconfigjson sweetrpg-registry \
#    --from-file=.dockerconfigjson

echo "NewRelic and logging config..."
kubectl create -n "${ns}" secret generic shared-web-files \
    --from-file=newrelic.ini

echo "Other secrets..."
kubectl create -n "${ns}" secret generic shared-web-cache \
    --from-env-file=cache.env
kubectl create -n "${ns}" secret generic shared-web-auth \
    --from-env-file=auth.env
kubectl create -n "${ns}" secret generic shared-web-misc \
    --from-env-file=misc.env
kubectl create -n "${ns}" secret generic shared-web-common \
    --from-env-file=../common.env

popd

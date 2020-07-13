#!/bin/bash

# How to run this script:
#  chmod +x ./server.sh
#  ./server.sh [one of the MODE cases shown below]

MODE=$1

cd react-app
npm run build
cd ..
cp -r react-app/build/* src/main/webapp

case $MODE in
     run)
          mvn package appengine:run
          ;;
     deploy-dev)
          mvn package appengine:deploy -Dapp.deploy.version=dev
          ;;
     deploy-prod)
          mvn package appengine:deploy -Dapp.deploy.version=prod
          ;;
esac

#!/bin/bash

# How to run this script:
#  chmod +x ./server.sh
#  ./server.sh [one of the MODE cases shown below]

MODE=$1

cd react_app
npm install  
npm run build
cd ..
cp -r react_app/build/* src/main/webapp

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

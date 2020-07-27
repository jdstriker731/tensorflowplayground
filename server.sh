#!/bin/bash

# How to run this script:
#  chmod +x ./server.sh
#  ./server.sh [one of the MODE cases shown below]

MODE=$1

CYAN_TEXT='\033[0;36m';
LIGHT_CYAN_TEXT='\033[1;36m';
RED_TEXT='\033[0;31m';
DEFAULT_TEXT='\033[0m';


build_react_app() {
    echo -e "\n${CYAN_TEXT}Running ${LIGHT_CYAN_TEXT}npm install${CYAN_TEXT}...${DEFAULT_TEXT}\n";
    cd react_app;
    npm install;
    echo -e "\n${CYAN_TEXT}Building React app...${DEFAULT_TEXT}\n";
    npm run build;
    cd ..;
    echo -e "\n${CYAN_TEXT} Copying React app into Servlet...${DEFAULT_TEXT}\n";
    cp -r react_app/build/* src/main/webapp;
}


case $MODE in
     run)
          build_react_app;
          mvn package appengine:run
          ;;
     deploy)
          if [ -z ${2+x} ]; then
              echo -e "\n\t${RED_TEXT} When deploying, version name is required as a positional argument!${DEFAULT_TEXT}\n";
              echo -e $"\tFor example, try:\n\t./server.sh $MODE $USER-dev\n";
              exit 1;
          fi;
          build_react_app;
          mvn package appengine:deploy -Dapp.deploy.version=dev
          ;;
     *)
          echo -e $"\n\t${RED_TEXT}You selected \"$MODE\", which is not a valid mode. ${DEFAULT_TEXT}Choose one of: {run|deploy}.\n";
          exit 1;
esac

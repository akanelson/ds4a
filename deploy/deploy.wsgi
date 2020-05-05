#!/bin/bash

REPODIR="/var/www/practicum"

json_resp() {
    echo '{"result":"'"$([[ $1 -eq 0 ]] && echo "success" || echo "failure")"'"}'
}

POSTJSON="$(cat -)"

#REPOURL="$(jq -r ".repository.clone_url" <<< "$POSTJSON")"
#REPONAME="$(jq -r ".repository.name" <<< "$POSTJSON")"

echo "Content-type: text/json"
echo ""

if [ -d $REPODIR ]; then
    cd $REPODIR
    sudo git pull
    json_resp $?
fi
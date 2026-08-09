#!/bin/bash

update_cmd="sf project deploy start --source-dir force-app/main/default/lwc/websocketConsole --target-org chat-scratch"

cd ./sf-chat-app
eval $update_cmd
cd ..
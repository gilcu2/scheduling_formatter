#!/bin/bash

APP_FILE=${1:-app}

cd "$PROJECT_DIR"/src || exit
uvicorn "$APP_FILE":app --reload

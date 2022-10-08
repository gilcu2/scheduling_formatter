#!/bin/bash

APP_FILE=${1:-formatter_app}

cd "$PROJECT_DIR"/src || exit
uvicorn "$APP_FILE":app --reload

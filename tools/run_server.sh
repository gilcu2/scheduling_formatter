#!/bin/bash

cd $PROJECT_DIR/src || exit
uvicorn server:app --reload
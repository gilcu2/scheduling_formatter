#!/bin/bash

cd $PROJECT_DIR/src || exit
uvicorn app:app --reload

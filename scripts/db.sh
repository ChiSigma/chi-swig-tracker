#!/bin/bash
export FLASK_APP=../backend/src/app.py
python backend/db.py "$@"
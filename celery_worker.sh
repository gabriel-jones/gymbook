#!/bin/bash

source env.sh
celery -A app.celery worker -l INFO
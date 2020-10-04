#!/bin/bash

source env.sh
celery -A app.celery beat -l INFO
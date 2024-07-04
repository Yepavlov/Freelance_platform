#!/bin/bash


cd /freelancer_platform/src

celery -A config worker -l ${CELERY_LOG_LEVEL} --beat --scheduler django
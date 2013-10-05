#!/bin/bash
cd $(dirname "$0")

if [ -z $REFTAG_SITE ]
then
    echo "Starting the dev appserver..."
    dev_appserver.py .. &> appserver.log &
    sleep 3
fi

echo "Running the test..."
python -m unittest test_with_browser test_jsonp_api

if [ -z $REFTAG_SITE ]
then
    echo "Stopping the dev appserver..."
    kill $!
fi

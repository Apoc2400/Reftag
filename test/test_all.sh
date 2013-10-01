#!/bin/bash
cd $(dirname "$0")

echo "Starting the dev appserver..."
dev_appserver.py .. &> appserver.log &
sleep 3

echo "Running the test..."
python -m unittest test_with_browser test_jsonp_api

echo "Stopping the dev appserver..."
kill $!

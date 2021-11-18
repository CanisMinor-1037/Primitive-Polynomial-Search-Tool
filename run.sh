#!/bin/bash
echo 'Installing python3.9-venv...'
sudo apt-get install python3.9 python3.9-venv
python3 -m venv venv
source ./venv/bin/activate
echo 'Installing flask...'
python -m pip install flask
echo 'Installing flask-bootstrap...'
python -m pip install flask-bootstrap
echo 'Installing flask-wtf...'
python -m pip install flask-wtf
echo 'Installing galois...'
python -m pip install galois
echo 'Done'

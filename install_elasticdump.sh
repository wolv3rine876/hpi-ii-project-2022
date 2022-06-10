#!/bin/bash
echo 'installing npm';
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -;
sudo apt-get install -y nodejs;

echo 'installing elastic dump';
sudo npm install elasticdump -g;
echo 'done';
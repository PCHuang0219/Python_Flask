#!/bin/bash

cd /var/jlo/sonic-mgmt/ansible/

#Add the topology to be testbed
./testbed-cli.sh add-topo $1 password.txt

#Generate minigraph and deploy minigraph to DUT
./testbed-cli.sh deploy-mg $1 lab password.txt

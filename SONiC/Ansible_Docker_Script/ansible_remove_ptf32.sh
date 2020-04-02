#!/bin/bash

cd /var/jlo/sonic-mgmt/ansible/

#Remove previous topology to be tested
./testbed-cli.sh remove-topo ptf1-32 password.txt
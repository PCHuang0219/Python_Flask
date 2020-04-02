#!/bin/bash

cd /var/jlo/sonic-mgmt/ansible/

#Reboot Dut
ansible-playbook -i lab --limit str-dut-01 test_sonic.yml -e testbed_name=$1 -e testcase_name=reboot 2>&1

#Verify DUT minigraph
# ./testbed-cli.sh test-mg $1 lab password.txt

#!/bin/bash

cd /var/jlo/sonic-mgmt/ansible/
ansible-playbook -i lab --limit str-dut-01 test_sonic.yml -e testbed_name=$1 -e testcase_name=$2 -vvv 2>&1

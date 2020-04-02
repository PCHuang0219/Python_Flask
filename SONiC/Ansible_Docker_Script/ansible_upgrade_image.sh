#!/bin/bash

cd /var/jlo/sonic-mgmt/ansible/

ansible-playbook upgrade_sonic.yml -i lab -l $1 -e "upgrade_type=sonic" -e "image_url='$2'"
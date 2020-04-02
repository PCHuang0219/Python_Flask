#!/bin/bash

echo "==========================  Docker start  ============================="

#sudo -S systemctl start docker << EOF 

#sonic

#EOF



docker start anber-test
#echo "==========================  Copy script to docker sonic-test from testbed  =========="

docker cp /home/jlo/source/back_end_server/SONiC/Ansible_Docker_Script f5af3e118a9b:/var/jlo
docker exec -i f5af3e118a9b sudo chmod 777 -R Ansible_Docker_Script
#echo "==========================  Remove all topology on DUT  ==================="

#docker exec -i -t 83c018229d2f /var/polly_hsu/run/ansible_remove_topology.sh

#Add topology

echo "==========================  Add test topology on DUT  ==================="

docker exec -i f5af3e118a9b sh /var/jlo/Ansible_Docker_Script/ansible_add_topology.sh ptf1-32
echo "==========================  Verify DUT minigraph  ======================="

docker exec -i f5af3e118a9b sh /var/jlo/Ansible_Docker_Script/ansible_verify_DUT.sh ptf1-32
echo "==========================  Run test case  =============================="

docker exec -i f5af3e118a9b sh /var/jlo/Ansible_Docker_Script/ansible_run_testcase.sh ptf1-32 iface_mode | tee ./../../report/5d1c4e5f7da4c511e89b53c8/TC046_ptf1-32_org_log.txt

#!/bin/bash
echo "==========================  Docker start  ============================="
#sudo -S systemctl start docker << EOF 
#sonic
#EOF

docker start sonic-test
#echo "==========================  Copy script to docker sonic-test from testbed  =========="
docker cp /home/sonic/flask_server/run 83c018229d2f:/var/polly_hsu
docker exec -i -t 83c018229d2f sudo chmod 777 -R run
#echo "==========================  Remove all topology on DUT  ==================="
#docker exec -i -t 83c018229d2f /var/polly_hsu/run/ansible_remove_topology.sh
#Add topology
echo "==========================  Add test topology on DUT  ==================="
docker exec -i -t 83c018229d2f /var/polly_hsu/run/ansible_add_topology.sh $1
echo "==========================  Verify DUT minigraph  ======================="
docker exec -i -t 83c018229d2f /var/polly_hsu/run/ansible_verify_DUT.sh 
echo "==========================  Run test case  =============================="
docker exec -i -t 83c018229d2f /var/polly_hsu/run/ansible_run_testcase.sh $1 $3 | tee /home/sonic/ansible_report/TC$2_$1_log.txt

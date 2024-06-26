#!/usr/bin/bash
cd /root/ansible
ansible-playbook -i hosts ./ha_playbook.yaml 
